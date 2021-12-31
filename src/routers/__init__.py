from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required

from src import User, bcrypt
from src.models import UserModel

view = Blueprint(
    "view",
    __name__,
    url_prefix="/api/v1"
)
user_model = UserModel()


@view.route("/")
def index():
    return "hello"


@view.route("/signIn")
def sign_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).one_or_none()
    if user is not None and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user)
        return jsonify(message="success", token=access_token), 200
    else:
        return jsonify(message="wrong email or password"), 401


@view.route("/signUp")
def sign_up():
    if request.method == "POST":
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        if user_model.sign_up(username, email, password):
            return ""
        else:
            return ""
    else:
        return jsonify(message="method not allowed by server"), 401


@view.route("welcome")
@jwt_required()
def welcome():
    return ""
