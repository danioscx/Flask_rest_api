from dataclasses import asdict
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from src.models.products import ProductImages, Products
from src.utils import object_to_list
from werkzeug.utils import secure_filename

products = Blueprint(
    "products",
    __name__,
    url_prefix="/api/v1/product"
)

"""
TODO implementation all method
"""

@products.route("/")
@jwt_required(optional=True)
def get_product():
    _products = Products.query.all()
    return object_to_list(_products)


@products.route("/<int:id>")
@jwt_required(optional=True)
def get_product(id):
    return jsonify(asdict(Products.query.get(id)))


@products.route('/add', methods=['POST'])
@jwt_required
def add_product():
    if request.method != 'POST':
        return jsonify({
            'message': 'invalid method'
        }), 503
    else:
        name = request.json.get("name", None)
        stock = request.json.get("stock", None)
        price = request.json.get("price", None)
        description = request.json.get("description", None)
        images_files = request.files.getlist('images')
        product_images = []
        if (len(images_files) > 5):
            return jsonify({
                'message': 'max 5 images'
            }), 409
        else:
            for images in images_files:
                filename = secure_filename(images.filename)
                product_images.append(ProductImages(image_url=images.filename))
            pass
        
        pass


@products.route("/edit/<int:id>", methods=['PATCH'])
@jwt_required
def edit_product(id):
    pass


@products.route("/delete/<int:id>", methods=['DELETE'])
@jwt_required
def delete_product(id):
    pass


@products.route("/add/to/favorite", methods=['PUT'])
@jwt_required
def add_to_favorite():
    pass


@products.route("/delete/from/favorite", methods=['DELETE'])
@jwt_required
def delete_from_favorite():
    pass


@products.route("/add/to/cart", methods=['PUT'])
@jwt_required
def add_to_cart():
    pass


@products.route("/delete/from/cart", methods=['DELETE'])
@jwt_required
def delete_from_cart():
    pass


@products.route("/cart/quantity", methods=['PATCH'])
@jwt_required
def increase_quantity():
    pass


@products.route("/cart/get")
@jwt_required
def get_cart():
    pass
