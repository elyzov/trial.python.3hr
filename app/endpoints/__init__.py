from .products import products_blueprint


def register_blueprints(app):
    app.register_blueprint(products_blueprint)
