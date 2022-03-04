from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catering.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__='customer'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('Name', db.String())
    phone = db.Column('Phone', db.String())

    def __repr__(self):
        return f'''<Customer Name: {self.name} Customer Phone: {self.phone}>'''


class Order(db.Model):
    __tablename__='order'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('Name', db.String())
    price = db.Column('Price',db.Integer())
    qty = db.Column('Qty',db.Integer())
    customer_id = db.Column(db.Integer(), db.ForeignKey('customer.id'),
                            nullable=False)
    customer = db.relationship('Customer',
                                backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f'Name: {self.name}, price: ${self.price/100}, qty: {self.qty}'


class Dish(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column('URL', db.String())
    alt = db.Column('ALT Text', db.String())
    name = db.Column('Name', db.String())
    ingredients = db.Column('Ingredients', db.String())
    price = db.Column('Price',db.Integer())
    
    def __repr__(self):
            return f'Name: {self.name}, price: ${self.price/100}'