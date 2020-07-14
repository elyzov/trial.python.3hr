from flask import Blueprint, jsonify

from app.models.products import Product

products_blueprint = Blueprint('products', __name__)


@products_blueprint.route('/products', methods=['GET'])
def get_products():
    return jsonify({
        'results': [p.serialized for p in Product.query.all()]
    })
