from dataclasses import asdict
from flask import Blueprint, jsonify, request

from src.models.merchants import Merchants, OpenTime
from src.utils import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt


merchants = Blueprint("merchants", __name__, url_prefix="/api/v1/merchants")


@merchants.route("/signup/merchant", methods=["PUT"])
def signup():
    if request.method != "PUT":
        return jsonify(message="invalid method"), 503
    else:
        name = request.json.get("name", None)
        email = request.json.get("email", None)
        username = request.json.get("username", None)
        address = request.json.get("address", None)
        phone_number = request.json.get("phone_number", None)
        password = request.json.get("password", None)
        if name is not None and email is not None and username is not None and address is not None and phone_number is not None and password is not None:
            merchant = Merchants(name=name, email=email, username=username,
                                 address=address, phone_number=phone_number, password=password)
            db.session.add(merchant)
            db.session.commit()
            return jsonify(message="merchant created"), 201
        else:
            return jsonify(message="missing fields"), 409


@merchants.route("/signin/merchant", methods=["POST"])
def signin():
    if request.method != "POST":
        return jsonify(message="invalid method"), 503
    else:
        email = request.json.get("email", None)
        phone_number = request.json.get("phone_number", None)
        password = request.json.get("password", None)
        if email is None:
            merchant = Merchants.query.filter_by(
                phone_number=phone_number).one_or_none()
        else:
            merchant = Merchants.query.filter_by(email=email).one_or_none()
        if merchant is not None and bcrypt.check_password_hash(merchant.password, password):
            addtional_claims = {"aud": "Merchant"}
            access_token = create_access_token(
                identity=merchant, additional_claims=addtional_claims)
            return jsonify(message="merchant signed in", token=access_token), 200
        else:
            return jsonify(message="invalid credentials"), 401


@merchants.route("/whoami", methods=["GET"])
@jwt_required
def whoami():
    if request.method != "GET":
        return jsonify(message="invalid method"), 503
    else:
        merchant_id = get_jwt_identity()
        merchant = Merchants.query.filter_by(id=merchant_id).one_or_none()
        if merchant is not None:
            return jsonify(asdict(merchant)), 200
        else:
            return jsonify(message="merchant not found"), 409


@merchants.route("/general/update", methods=["PATCH"])
@jwt_required
def update_address():
    audience = get_jwt()
    if request.method != "PATCH":
        return jsonify(message="invalid method"), 503
    elif audience["aud"] != "Merchant":
        return jsonify(message="unauthorized"), 403
    else:
        merchant_id = get_jwt_identity()
        merchant = Merchants.query.filter_by(id=merchant_id).one_or_none()
        name = request.json.get("name", None)
        address = request.json.get("address", None)
        username = request.json.get("username", None)
        if merchant is not None:
            merchant.name = name if name is not None else merchant.name
            merchant.address = address if address is not None else merchant.address
            merchant.username = username if username is not None else merchant.username
            db.session.commit()
            return jsonify(message="merchant updated"), 200
        else:
            return jsonify(message="merchant not found"), 409


@merchants.route("/update/phone", methods=["PATCH"])
@jwt_required
def update_phone_number():
    audience = get_jwt()
    if request.method != "PATCH":
        return jsonify(message="invalid method"), 503
    elif audience["aud"] != "Merchant":
        return jsonify(message="unauthorized"), 403
    else:
        merchant_id = get_jwt_identity()
        merchant = Merchants.query.filter_by(id=merchant_id).one_or_none()
        phone_number = request.json.get("phone_number", None)
        if merchant is not None:
            merchant.phone_number = phone_number if phone_number is not None else merchant.phone_number
            db.session.commit()
            return jsonify(message="merchant updated"), 200
        else:
            return jsonify(message="merchant not found"), 409


@merchants.route("/update/password", methods=["PATCH"])
@jwt_required
def update_password():
    audince = get_jwt()
    if request.method != 'PATCH':
        return jsonify(message="invalid method"), 503
    elif audince["aud"] != "Merchant":
        return jsonify(message="unauthorized"), 403
    else:
        password = request.json.get("password", None)
        if password is None or len(password) < 8:
            return jsonify(message="missing fields"), 409
        else:
            merchant_id = get_jwt_identity()
            merchant = Merchants.query.filter_by(id=merchant_id).one_or_none()
            if merchant is not None:
                merchant.password = bcrypt.generate_password_hash(password)
                db.session.commit()
                return jsonify(message="merchant updated"), 200
            else:
                return jsonify(message="merchant not found"), 409


@merchants.route("/update/email", methods=["PATCH"])
@jwt_required
def update_email():
    audience = get_jwt()
    if request.method != "PATCH":
        return jsonify(message="invalid method"), 503
    elif audience != "Merchant":
        return jsonify(message="unauthorized"), 403
    else:
        email = request.json.get("email", None)
        if email is None or email.count("@") != 1:
            return jsonify(message="missing fields"), 409
        else:
            merchant_id = get_jwt_identity()
            merchant = Merchants.query.filter_by(id=merchant_id).one_or_none()
            if merchant is not None:
                merchant.email = email
                db.session.commit()
                return jsonify(message="merchant updated"), 200
            else:
                return jsonify(message="merchant not found"), 409


@merchants.route("/update/open-time", methods=["PATCH"])
@jwt_required
def update_open_time():
    audience = get_jwt()
    if request.method != "PATCH":
        return jsonify(message="invalid method"), 503
    elif audience != "Merchant":
        return jsonify(message="unauthorized"), 403
    else:
        day = request.json.get("day", None)
        status = request.json.get("status", None)
        start_time = request.json.get("start_time", None)
        end_time = request.json.get("end_time", None)
        if day is None or start_time is None or end_time is None:
            return jsonify(message="missing fields"), 409
        else:
            open_time = OpenTime(
                day=day,
                status=status,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(open_time)
            db.session.commit()
            return jsonify(message="open time added"), 200
