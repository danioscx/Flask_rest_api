from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_current_user

from src import User, bcrypt
from src.models.user_model import UserModel

view = Blueprint(
    "view",
    __name__,
    url_prefix="/api/v1"
)

model = UserModel()


@view.route("/")
def index():
    user = model.get_users()
    return jsonify(user)


@view.route("/signin", methods=['POST'])
def sign_in():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).one_or_none()
    if user is not None and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user)
        return jsonify(message="success", token=access_token), 200
    else:
        return jsonify(message="wrong email or password"), 401


@view.route("/signup", methods=['POST'])
def sign_up():
    if request.method == "POST":
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        if model.create_user(username, email, password):
            return jsonify(message="success sign up"), 200
        else:
            return jsonify(message="error"), 409
    else:
        return jsonify(message="method not allowed by server"), 401


@view.route("welcome")
@jwt_required()
def welcome():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).one_or_none()
    return jsonify(user), 200
