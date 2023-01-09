from sqlalchemy_mptt.mixins import BaseNestedSets
from flask_login import UserMixin

from app import db, manager


# Таблица пользователей

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Таблицы продуктов

class Category(db.Model, BaseNestedSets):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), index=True, unique=True)
    url = db.Column(db.String, unique=True)
    text = db.Column(db.String(2000)) #new
    title = db.Column(db.String(200))
    description = db.Column(db.String(300))
    image = db.relationship("Images", cascade="all,delete", backref='image', lazy='dynamic')
    items = db.relationship("Product", cascade="all,delete", backref="item")


    def __repr__(self):
        return '<Categoryy {}>'.format(self.name)

subs = db.Table('subs',
                db.Column('product_id', db.ForeignKey('products.id')),
                db.Column('suggestion_id', db.ForeignKey('suggestion.id'))
)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    name = db.Column(db.String(475), index=True)
    url = db.Column(db.String)
    intro = db.Column(db.Text(1500))
    text = db.Column(db.Text(1500))
    title = db.Column(db.String(200)) #new
    description = db.Column(db.String(300)) #new
    keys = db.relationship("Keys", cascade="all,delete", backref='product') # new
    items = db.relationship("Images", cascade="all,delete", backref='item', lazy='dynamic')  # удаляет каскадно все таблицы
    # items = db.relationship("Images", backref=db.backref('item', cascade="all, delete-orphan"), lazy='dynamic')
    price = db.relationship("Price", cascade="all,delete", backref='product', lazy='dynamic')
    sugg = db.relationship("Suggestion", cascade="all,delete", backref='product1', lazy='dynamic')
    suggestion = db.relationship("Suggestion", cascade="all,delete", secondary=subs, backref=db.backref('product'))
    index_prod = db.relationship("Index_product", cascade="all,delete", backref='product')


class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    filename = db.Column(db.String(300))
    alt = db.Column(db.String(100)) # new

class Keys(db.Model):
    __tablename__ = 'keys'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text(1500))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    images = db.relationship("Images_key", cascade="all,delete", backref='keys')

class Images_key(db.Model):
    __tablename__ = 'images_key'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    alt = db.Column(db.String(100))
    keys_id = db.Column(db.Integer, db.ForeignKey('keys.id'))

class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True)
    name_price = db.Column(db.String)
    price = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

class Suggestion(db.Model):
    __tablename__ = 'suggestion'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


# Главная страница

class Social(db.Model):
    __tablename__ = 'social'
    id = db.Column(db.Integer, primary_key=True)
    telegram = db.Column(db.String)
    whatsap = db.Column(db.String)
    phone1 = db.Column(db.String)
    phone2 = db.Column(db.String)
    phone3 = db.Column(db.String)
    phone4 = db.Column(db.String)
    phone5 = db.Column(db.String)
    phone6 = db.Column(db.String)
    email = db.Column(db.String)
    title = db.Column(db.String(200)) #new
    description = db.Column(db.String(300)) #new

class Index_product(db.Model):
    __tablename__ = 'index_product'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
