import os
from dataclasses import asdict

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message

from src.account.models.account import Account
from src.account.services.account_services import get_user
from src.utils import bcrypt, db, mail_app, PasswordUtils

account = Blueprint('user_controller', __name__, url_prefix='/api/v1/account')


@account.route('/signin', methods=['POST'])
def signin():
    if request.method == 'POST':
        username = request.json.get('username_or_email', None)
        password = request.json.get('password', None)
        user = Account.query.filter_by(username=username).one_or_none() or Account.query.filter_by(
            email=username).one_or_none()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user)
            return jsonify(message="success signin", token=access_token), 200
        else:
            return jsonify(message="failed signin"), 401
    else:
        return jsonify(message="method not allowed"), 503


@account.route('/signup', methods=['PUT', 'POST'])
def signup():
    if request.method == 'POST' or request.method == 'PUT':
        name = request.json.get('name', None)
        email = request.json.get('email', None)
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        date_of_birth = request.json.get('date_of_birth', None)
        if name is None or username is None or email is None or password is None or date_of_birth is None:
            return jsonify(message="missing fields"), 409
        user = Account.query.filter_by(username=username).one_or_none() or Account.query.filter_by(
            email=email).one_or_none()
        if user is not None:
            return jsonify(message="account already exists"), 409
        else:
            user = Account(username=username, email=email, password=bcrypt.generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return jsonify(message="success signup"), 201
    else:
        return jsonify(message="method not allowed"), 503


@account.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        user_id = get_jwt_identity()
        user = Account.query.filter_by(id=user_id).one_or_none()
        if user is not None:
            return jsonify(asdict(user)), 200
        else:
            return jsonify(message="account not found"), 404


@account.route('/settings', methods=['PATCH', 'POST'])
@jwt_required()
def setting():
    if request.method == 'PATCH' or request.method == 'POST':
        user_id = get_jwt_identity()
        user = Account.query.filter_by(id=user_id).one_or_none()
        if user is not None:
            name = request.json.get('name', None)
            email = request.json.get('email', None)
            username = request.json.get('username', None)
            phone_number = request.json.get('phone_number', None)
            date_of_birth = request.json.get('date_of_birth', None)
            if name is not None:
                user.name = name
            if email is not None:
                user.mail_app = email
            if username is not None:
                user.username = username
            if phone_number is not None:
                user.phone_number = phone_number
            if date_of_birth is not None:
                user.date_of_birth = date_of_birth
            db.session.commit()
            return jsonify(message="success update"), 200
        else:
            return jsonify(message="account not found"), 404
    else:
        return jsonify(message="method not allowed"), 503


password_utils = PasswordUtils()


@account.route('/setting/update/password', methods=['PATCH'])
@jwt_required()
def update_password():
    if request.method == 'PATCH':
        user_id = get_jwt_identity()
        user = Account.query.filter_by(id=user_id).one_or_none()
        if user is not None:
            current_password = request.json.get('current_password', None)
            new_password = request.json.get('password', None)
            if new_password is not None and current_password is None and bcrypt.check_password_hash(
                    user.password, current_password
            ):
                try:
                    password_utils.set_password(new_password)
                    password_utils.set_code_generator(6)
                    message = Message(
                        subject="Request to change password",
                        recipients=user.mail_app,
                        sender=os.environ.get('DEFAULT_MAIL_SENDER', None),
                        body="Please do not give this code to anyone else. {}".format(
                            password_utils.get_code_generator())
                    )
                    mail_app.send(message)
                    return jsonify(message="success update"), 200
                except KeyError as e:
                    return jsonify(message='email sender not set {}'.format(e)), 409
            else:
                return jsonify(message="missing fields"), 409
        else:
            return jsonify(message="account not found"), 404
    else:
        return jsonify(message="method not allowed"), 503


@account.route('/setting/password/verify', methods=['POST'])
@jwt_required()
def verify_password():
    """
    if request method is post
    """
    if request.method == 'POST':  # check if the request is post
        user_id = get_jwt_identity()
        user = get_user(user_id)
        if user is not None:
            code = request.json.get('code', None)
            if code is not None and code == password_utils.get_code_generator():
                if password_utils.get_password() is not None:
                    user.password = bcrypt.generate_password_hash(password_utils.get_password())
                    db.session.commit()
                    return jsonify(message="success update"), 200
                else:
                    return jsonify(message="missing fields"), 409
            else:
                return jsonify(message="invalid code"), 409
        else:
            return jsonify(message="account not found"), 404
    else:
        return jsonify(message="method not allowed"), 503
