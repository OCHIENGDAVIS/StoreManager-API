import jwt
import datetime
import os
from flask import request, jsonify, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.v1.models.user_models import User
from app.api.v1.utils import validate_user, validate_login
from functools import wraps

user_object = User()
user_dec = Blueprint('v1_user', __name__)
os.environ['SECRET'] = 'hello-there-its-allan'


def login_token(f):
    """All endpoints that need log in will be wrapped by this decorator"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'Message': 'You need to log in'}), 401
        try:
            data = jwt.decode(token, os.getenv('SECRET'), options={'verify_exp': False})
            if data['email'] in user_object.u_token:
                current_user = user_object.users[data['email']]
            else:
                return jsonify({"Message": "Token expired:Login again"}), 401
        except BaseException:
            return jsonify({'Message': 'Invalid request!Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# noinspection PyMethodParameters
class UserViews(object):
    def __init__(self, current_user):
        self.current_user = current_user

    def __getitem__(self, item):
        return self.current_user[item]

    @user_dec.route('/api/v1/auth/register', methods=['POST'])
    def create_user():
        """receive user input as json object"""
        data = request.get_json()
        if data['email'] in user_object.users:
            return jsonify({'Message': "User already exists"}), 400
        if validate_user(data):
            return validate_user(data)
        password_hash = generate_password_hash(data['password'], method='sha256')
        user_object.create_user(data['email'], password_hash)
        return jsonify({"Message": "User registered successfully"}), 201

    @user_dec.route('/api/v1/auth/login', methods=['POST'])
    def login():
        """Log in and generate token"""
        auth = request.get_json()
        user = user_object.users[auth['email']]
        if auth['email'] not in user_object.users.keys():
            return jsonify({"Message": "Email not found!"}), 401
        if validate_login(auth):
            return validate_login(auth)
        if check_password_hash(user['password'], auth['password']):
            session['loggedin'] = True
            session['email'] = auth['email']
            token = jwt.encode(
                dict(email=user['email'], exp=datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)),
                os.getenv('SECRET'))
            user_object.u_token[user['email']] = token
            return jsonify({"token": token.decode('UTF-8')}), 200
        return jsonify({"Message": "login invalid!"}), 401

    @user_dec.route('/api/v1/auth/logout', methods=['DELETE'])
    @login_token
    def logout(current_user):
        """Destroy user session"""
        if session and session['loggedin']:
            session.clear()
            return jsonify({"Message": "logged out"}), 200
        return jsonify({"Message": "Already logged out"}), 400

    @user_dec.route('/api/v1/auth/reset-password', methods=['PUT'])
    @login_token
    def reset_password(current_user):
        """Requires the user to be logged in to change password"""
        data = request.get_json()
        password_hash = generate_password_hash(data['password'], method='sha256')
        usr = user_object.users[current_user["email"]]
        usr.update({"password": password_hash})
        return jsonify({"Message": "password updated"}), 202

    @user_dec.route('/api/v1/auth/users', methods=['GET'])
    @login_token
    def get_all_users(current_user):
        return jsonify({"users": user_object.users}), 200
