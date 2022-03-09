from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.users import ShippingAddress
from src.utils import db, object_to_list

address = Blueprint(
    "address",
    __name__,
    url_prefix="/api/v1/address"
)


@address.route("/add", methods=['PUT', 'GET'])
@jwt_required()
def add():
    if request.method != 'PUT':
        return jsonify({
            "message": 'not found'
        }), 404
    else:
        user_id = get_jwt_identity()
        recipient_name = request.json.get('recipient_name', None)
        address = request.json.get('address', None)
        get_address = ShippingAddress.query.filter(ShippingAddress.user_id == user_id).filter(
            ShippingAddress.active == True
        ).one_or_none()
        if get_address is not None:
            shipping_address = ShippingAddress(
                address=address, recipient_name=recipient_name, active=False, user_id=user_id)
        else:
            shipping_address = ShippingAddress(
                address=address, recipient_name=recipient_name, active=True, user_id=user_id)
        db.session.add(shipping_address)

        try:
            db.session.commit()
            return jsonify({
                "message": "success insert address"
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "message": "error {}".format(e),
            }), 409


@address.route("/update/<int:id>", methods=['PATCH', 'GET'])
@jwt_required()
def update(id: int):
    if request.method != 'PATCH':
        return jsonify({
            'message': 'method not allowed'
        }), 503
    else:
        address = request.json.get('address', None)
        recipient_name = request.json.get('recipient_name', None)
        active = request.json.get('active', None)
        get_address = ShippingAddress.query.filter_by(id=id).first()
        get_address.address = address
        get_address.recipient_name = recipient_name
        get_address.active = active
        try:
            db.session.commit()
            return jsonify({
                'message': 'success update address'
            }), 200
        except Exception as e:
            return jsonify({
                'message': 'unable update address {}'.format(e)
            })


@address.route("/delete/<int:id>", methods=['DELETE', 'GET'])
@jwt_required()
def delete(id: int):
    if request.method != 'DELETE':
        return jsonify({
            'message': 'method not alowed'
        }), 503
    else:
        address = ShippingAddress.query.filter_by(id=id).first()
        try:
            db.session.delete(address)
            db.session.commit()
            return jsonify({
                'message': 'success delete address'
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'message': 'failed delete address {}'.format(e)
            }), 409


@address.route("/get", methods=['GET'])
@jwt_required()
def get():
    user_id = get_jwt_identity()
    address = ShippingAddress.query.filter(ShippingAddress.user_id == user_id).all()
    return jsonify(object_to_list(address))
