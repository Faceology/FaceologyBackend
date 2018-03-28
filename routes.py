import requests
from collections import Counter
from models import *
from flask import json
from flask import Flask, Response, jsonify, abort, make_response, request, g, send_from_directory
from flask_restful import Resource, Api, reqparse, inputs
from flask_httpauth import HTTPBasicAuth
from config import app, session, port_num, riot_key
from werkzeug.exceptions import Unauthorized
from matching import sort_matches

auth = HTTPBasicAuth()
my_api = Api(app)

class User(Resource):
    def __init__(self):
        # used for auth
        self.reqparse = reqparse.RequestParser()

    # getting a user via id (expand this later as necessary)
    @auth.login_required
    def get(self):
        return jsonify({'hello' : 'world'})

# Define resource-based routes here
my_api.add_resource(User, '/api/user', endpoint = 'user')

# main server run line
if __name__ == '__main__':
    app.run(debug=True, port = port_num, host = '0.0.0.0')

