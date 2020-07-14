from flask import Blueprint, jsonify, request, current_app, make_response
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.endpoints.invalid_usage import InvalidUsage
from app.models.products import Product

products_blueprint = Blueprint('products', __name__)


def jsonify_no_content():
    response = make_response('', 204)
    response.mimetype = current_app.config['JSONIFY_MIMETYPE']
    return response


@products_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@products_blueprint.route('/products', methods=['GET'])
def get_products():
    return jsonify({
        'results': [p.serialized for p in Product.query.all()]
    })


@products_blueprint.route('/products', methods=['POST'])
def create_product():
    payload = request.json
    current_app.logger.debug(f'got payload = {payload}')
    try:
        product = Product.create(payload)
        return jsonify(product.serialized), 201
    except Exception as e:
        raise InvalidUsage(f'An error accrued: {e}', 410)


@products_blueprint.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    payload = request.json
    current_app.logger.debug(f'got payload = {payload}')
    try:
        product = Product.update(id, payload)
        return jsonify(product.serialized)
    except NoResultFound:
        raise InvalidUsage(f'Product with id {id} not found', 404)
    except Exception as e:
        raise InvalidUsage(f'An error accrued: {e}', 410)


@products_blueprint.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    try:
        product = Product.retrieve(id)
        return jsonify(product.serialized)
    except NoResultFound:
        raise InvalidUsage(f'Product with id {id} not found', 404)
    except Exception as e:
        raise InvalidUsage(f'An error accrued: {e}', 410)


@products_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        Product.delete(id)
        return jsonify_no_content()
    except Exception as e:
        raise InvalidUsage(f'An error accrued: {e}', 410)
