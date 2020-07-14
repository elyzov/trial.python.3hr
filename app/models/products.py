from flask import current_app
from sqlalchemy.orm import validates

from app import db
import datetime


class InvalidPayload(Exception):
    """Raised when the got invalid payload"""
    pass


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Unicode(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    featured = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    expiration_date = db.Column(db.DateTime, nullable=True)

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    categories = db.relationship('Category', secondary='products_categories', backref='products')

    items_in_stock = db.Column(db.Integer, nullable=False)
    receipt_date = db.Column(db.DateTime, nullable=True)

    @validates('name')
    def validate_name(self, key, name):
        current_app.logger.debug(f'validate product name: key = {key}, name = {name}')
        name_len = len(name)
        if name_len < 0 or 50 < name_len:
            raise ValueError(f'[name] expected length between 1-50, got {name_len}')
        return name

    @validates('featured')
    def validate_featured(self, key, featured):
        current_app.logger.debug(f'validate product featured: key = {key}, featured = {featured}')
        if not isinstance(featured, bool):
            raise ValueError(f'[featured] boolean is expected, but got {type(featured).__name__} ({featured})')
        return featured

    @validates('rating')
    def validate_rating(self, key, rating):
        current_app.logger.debug(f'validate product rating: key = {key}, rating = {rating}')
        if rating < 0:
            raise ValueError(f'[rating] expected positive value, got {rating}')
        return rating

    @validates('items_in_stock')
    def validate_items_in_stock(self, key, items_in_stock):
        current_app.logger.debug(f'validate product items_in_stock: key = {key}, items_in_stock = {items_in_stock}')
        if items_in_stock < 0:
            raise ValueError(f'[items_in_stock] expected positive value, got {items_in_stock}')
        return items_in_stock

    def __str__(self):
        return f'({self.id}) {self.name}'

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'featured': self.featured,
            'items_in_stock': self.items_in_stock,
            'receipt_date': self.receipt_date,
            'brand': self.brand.serialized,
            'categories': [c.serialized for c in self.categories],
            'expiration_date': self.expiration_date,
            'created_at': self.created_at
        }

    @classmethod
    def prepare_values(cls, payload):
        values = {k: v for k, v in payload.items() if k in cls.__table__.columns}
        brand_name = payload.get('brand', None)
        if brand_name:
            brand = db.session.query(Brand).filter_by(name=brand_name).first()
            if not brand:
                raise InvalidPayload(f'got unknown brand {brand_name}')
            values['brand_id'] = brand.id
        categories = {
            name: db.session.query(Category).filter_by(name=name).first() for name in payload.get('categories', [])
        }
        for name, category in categories.items():
            if not category:
                raise InvalidPayload(f'got unknown category {name}')
        if categories:
            values['categories'] = [category for _, category in categories.items()]
        return values

    @classmethod
    def update(cls, id, payload):
        values = cls.prepare_values(payload)
        obj = db.session.query(Product).get(id)
        for k, v in values.items():
            setattr(obj, k, v)
        db.session.commit()
        return obj

    @classmethod
    def delete(cls, id):
        obj = db.session.query(Product).get(id)
        if obj:
            current_app.logger.debug(f'got product for delete {obj}')
            db.session.delete(obj)
            db.session.commit()

    @classmethod
    def retrieve(cls, id):
        return db.session.query(Product).filter_by(id=id).one()

    @classmethod
    def create(cls, payload):
        values = cls.prepare_values(payload)
        if not values.get('brand_id', None):
            raise InvalidPayload('brand is required')
        if not values.get('categories', []):
            raise InvalidPayload('categories is required')
        obj = cls(**values)
        db.session.add(obj)
        db.session.commit()
        return obj


class Brand(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=False)
    country_code = db.Column(db.Unicode(2), nullable=False)

    products = db.relationship('Product', backref='brand')

    def __str__(self):
        return f'({self.id}) {self.name}'

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code
        }


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(50), nullable=False)

    def __str__(self):
        return f'({self.id}) {self.name}'

    @property
    def serialized(self):
        return {
            'id': self.id,
            'name': self.name,
        }


products_categories = db.Table(
    'products_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)
