from dataclasses import asdict
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models.products import Cart, ProductImages, Products
from src.models.users import Favorites
from src.utils import object_to_list
from werkzeug.utils import secure_filename
from src.utils import db

products = Blueprint(
    "products",
    __name__,
    url_prefix="/api/v1/products"
)


@products.route("/<int:id>", methods=["GET"])
def get_product(id):
    if (id is None):
        return object_to_list(Products.query.all())
    else:
        return jsonify(asdict(Products.query.get(id).one_or_none()))


@products.route('/add', methods=['POST'])
@jwt_required
def add_product():
    if request.method != 'POST':
        return jsonify(message='invalid method'), 503
    else:
        name = request.json.get("name", None)
        stock = request.json.get("stock", None)
        price = request.json.get("price", None)
        description = request.json.get("description", None)
        images_files = request.files.getlist('images')
        product_images = []
        if (len(images_files) > 5):
            return jsonify({
                'message': 'max 5 images per product'
            }), 409
        else:
            for images in images_files:
                filename = secure_filename(images.filename)
                product_images.append(ProductImages(image_url=images.filename))


@products.route("/edit/<int:id>", methods=['PATCH'])
@jwt_required
def edit_product(id):
    pass


@products.route("/delete/<int:id>", methods=['DELETE'])
@jwt_required
def delete_product(id):
    product_id = Products.query.get(id).one_or_none()
    if product_id is None:
        return jsonify({
            "message": "product not found"
        }), 409
    else:
        db.session.delete(product_id)
        db.session.commit()
        return jsonify({
            "message": "product deleted"
        }), 200


@products.route("/favorite/add", methods=['PUT'])
@jwt_required
def add_to_favorite():
    if request.method != 'PUT':
        return jsonify(message='invalid method'), 503
    else:
        user_id = get_jwt_identity()
        product_id = request.json.get("product_id", None)
        product = Products.query.get(product_id).one_or_none()
        favorites = Favorites(user_id=user_id, product=product)
        db.session.add(favorites)
        db.session.commit()
        return jsonify({
            'message': 'product added to favorite'
        }), 200


@products.route("/favorite/delete", methods=['DELETE'])
@jwt_required
def delete_from_favorite():
    if request.method != 'DELETE':
        return jsonify(message='invalid method'), 503
    else:
        favorite_id = request.json.get("favorite_id", None)
        favorite = Favorites.query.get(favorite_id).one_or_none()
        if favorite is not None:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify(message='product deleted from favorite'), 200
        else:
            return jsonify(message='product not found'), 404


@products.route("/favorite/get", methods=['GET'])
@jwt_required
def get_favorites():
    user_id = get_jwt_identity()
    return object_to_list(Favorites.query.filter_by(user_id=user_id).all())


@products.route("/cart/add", methods=['PUT'])
@jwt_required
def add_to_cart():
    if request.method != 'PUT':
        return jsonify(message='invalid method'), 503
    else:
        user_id = get_jwt_identity()
        product_id = request.json.get("product_id", None)
        quantity = request.json.get("quantity", None)
        if product_id is None and quantity is None or quantity == 0:
            return jsonify(message='invalid input'), 409
        else:
            cart = Cart(user_id=user_id, product_id=product_id,
                        quantity=quantity)
            db.session.add(cart)
            db.session.commit()
            return jsonify(message='product added to cart'), 200


@products.route("/cart/delete", methods=['DELETE'])
@jwt_required
def delete_from_cart():
    cart_id = request.json.get("cart_id", None)
    cart = Cart.query.get(cart_id).one_or_none()
    if cart is not None:
        db.session.delete(cart)
        db.session.commit()
        return jsonify(message='product deleted from cart'), 200
    else:
        return jsonify(message='product not found'), 409


@products.route("/cart/quantity", methods=['PATCH'])
@jwt_required
def increase_quantity():
    cart_id = request.json.get("cart_id", None)
    quantity = request.json.get("quantity", None)
    cart = Cart.query.get(cart_id).one_or_none()
    if cart is not None:
        if quantity == 0:
            db.session.delete(cart)
            db.session.commit()
            return jsonify(message='product deleted from cart'), 200
        else:
            cart.quantity = quantity
            db.session.commit()
            return jsonify(message='product quantity updated'), 200
    else:
        return jsonify(message='product not found'), 409


@products.route("/cart/get")
@jwt_required
def get_cart():
    user_id = get_jwt_identity()
    return object_to_list(Cart.query.filter_by(user_id=user_id).all())
