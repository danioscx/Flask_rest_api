import json
from flask import Blueprint, jsonify, request

from src.models.users import ShippingAddress, Users
from src.utils import bcrypt, db, default_encoder
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


users = Blueprint(
    "users",
    __name__,
    url_prefix="/api/v1/user"
)


@users.route("/me", methods=['GET', 'POST'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    shipping_address = ShippingAddress.query.filter_by(
        user_id=user_id).one_or_none()
    if shipping_address is None:
        user = Users.query.filter_by(id=user_id).one_or_none()
    else:
        user = Users.query.join(
            ShippingAddress, Users.id == ShippingAddress.user_id
        ).filter(
            (ShippingAddress.active == True) |
            (Users.id == user_id)
        ).one_or_none()
    if user is not None:
        return json.dumps(user, default=default_encoder), 200
    else:
        return jsonify({'message': 'UnAuthorization'}), 403


@users.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.json.get("email", None)
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        try:
            if username is None:
                db.session.add(
                    Users(email=email, password=bcrypt.generate_password_hash(password)))
            elif email is None or password is None:
                return jsonify({
                    'message': 'username or password cannot be null'
                })
            else:
                db.session.add(Users(email=email, username=username,
                               password=bcrypt.generate_password_hash(password)))

            db.session.commit()
            return jsonify({
                'message': 'success created user'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'message': 'failed created user email is already usage {}'.format(e)
            }), 409
    else:
        return jsonify({
            'message': 'Method not allowed'
        }), 503


@users.route("/signin", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = Users.query.filter_by(email=email).one_or_none()
        if user is not None and bcrypt.check_password_hash(user.password, password):
            additonal_claims = {"aud": "User"}
            access_token = create_access_token(identity=user, additional_claims=additonal_claims)
            return jsonify({
                'message': 'success sign in',
                'token': access_token
            }), 200
        else:
            return jsonify({
                'message': 'invalid credential'
            }), 409
    else:
        return jsonify({
            'message': 'method not allowed'
        }), 503
