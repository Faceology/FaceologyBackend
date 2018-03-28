import requests
from collections import Counter
from models import *
from flask import json
from flask import Flask, Response, jsonify, abort, make_response, request, g, send_from_directory
from flask_restful import Resource, Api, reqparse, inputs
from flask_httpauth import HTTPBasicAuth
from config import app, session, port_num
from werkzeug.exceptions import Unauthorized

auth = HTTPBasicAuth()
my_api = Api(app)

class User(Resource):
    def __init__(self):
        # used for auth
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('email', type=str, location='json')
        self.reqparse.add_argument('password', type=str, location='json')

    def get(self):
        if session.query(User).filter_by(name = params['username']).first() is not None:
            abort(400, "That email already exists!")
        new_user = User(
            params['email']
        )
        session.add(new_user)
        session.commit()
        return jsonify({'hello' : 'world'})

# Define resource-based routes here
my_api.add_resource(User, '/api/user', endpoint = 'user')
my_api.add_resource(User, '/api/event', endpoint = 'event')
my_api.add_resource(User, '/api/info', endpoint = 'info')

# main server run line
if __name__ == '__main__':
    app.run(debug=True, port = port_num, host = '0.0.0.0')

