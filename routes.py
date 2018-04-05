import requests
from collections import Counter
from models import *
from flask import json
from flask import Flask, Response, jsonify, abort, make_response, request, g, send_from_directory
from flask_restful import Resource, Api, reqparse, inputs
from flask_httpauth import HTTPBasicAuth
from config import app, session, port_num, consumer_key, consumer_secret
from werkzeug.exceptions import Unauthorized

auth = HTTPBasicAuth()
my_api = Api(app)

class User(Resource):
    def __init__(self):
        # used for auth
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type=str, location='args', required=True)
        self.reqparse.add_argument('password', type=str, location='args', required=True)


class UserInfo(Resource):
    def __init__(self):
        # used for posting new user information
        self.match_reqparse = reqparse.RequestParser()
        self.match_reqparse.add_argument('eventKey', type=str, location='args', required=True)
        self.match_reqparse.add_argument('image', type=str, location='args', required=False)

        self.post_reqparse = reqparse.RequestParser()
        self.post_reqparse.add_argument('linkedinInfo', type=dict, location='json', required=True)
        self.post_reqparse.add_argument('eventKey', type=str, location='json', required=True)

    def get(self):
        params = self.match_reqparse.parse_args()
        event_id = session.query(Event).filter_by(event_key = params['eventKey']).first().as_dict()['event_id']
        event_users = session.query(EmployerInfo).filter_by(event_id = event_id).all()
        event_users = map(lambda user: user.as_dict(), event_users)
        best_match = find_best_match(event_users, params['image'])
        return jsonify({'bestMatch' : best_match})

    def post(self):
        params = self.post_reqparse.parse_args()
        linkedin_info = params['linkedinInfo']
        event_key = params['eventKey']

        # find matching event (validating QR code)
        event_id = None
        matched_event = session.query(Event).filter_by(event_key = event_key).first()
        if matched_event:
            event_id = matched_event.as_dict()['event_id']
        else:
            abort(400, 'No event matched this key!')

        #linkedin_info = application.get_profile(selectors=['id', 'formatted-name', 'location', 'num-connections', 'picture-urls::(original)', 'summary'])

        # add a user and their photo if they don't already exist
        matching_user = session.query(Entity).filter_by(name = linkedin_info['formattedName']).first()
        user_id = None
        if matching_user is None:
            if (linkedin_info['pictureUrls'] and linkedin_info['pictureUrls']['values'] > 0):
                new_user = Entity(str(linkedin_info['formattedName']), str(linkedin_info['pictureUrls']['values'][0]))
                session.add(new_user)
                session.commit()
                user_id = new_user.as_dict()['user_id']
            else:
                abort(400, 'No profile pictures for the authenticated user')
        else:
            user_id = matching_user.as_dict()['user_id']

        # add that user's linkedin info for a specific event, if it doesn't already exist
        if session.query(EmployerInfo).filter_by(user_id = user_id, event_id = event_id).first() is None:
            user_info = EmployerInfo(user_id, event_id, linkedin_info['summary'])
            session.add(user_info)
        session.commit()
        return "Success!"

class EventInfo(Resource):
    def __init__(self):
        # used for auth
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('eventKey', type=str, location='json', required=True)
        self.reqparse.add_argument('name', type=str, location='json', required=True)

    def post(self):
        params = self.reqparse.parse_args()
        new_event = None
        if session.query(Event).filter_by(event_key = params['eventKey']).first() is None:
            new_event = Event(params['eventKey'], params['name'])
            session.add(new_event)
        else:
            abort(400, 'event already exists!')
        session.commit()
        return jsonify({"eventAdded": new_event.as_dict()})

# Define resource-based routes here
my_api.add_resource(User, '/api/user', endpoint = 'user')
my_api.add_resource(UserInfo, '/api/userInfo', endpoint = 'info')
my_api.add_resource(EventInfo, '/api/event', endpoint = 'event')

# main server run line
if __name__ == '__main__':
    app.run(debug=True, port = port_num, host = '0.0.0.0')

