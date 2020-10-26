import datetime

from sqlalchemy_serializer import SerializerMixin

from app import db
from app.auth.models import AnonymousUser, User
from app.utils import ModelMixin


class Client(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-sales', '-comings', '-balances' )
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.BigInteger, unique=True)
    productname = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    comment = db.Column(db.Text)
    sale = db.relationship('Sale', backref='client')
    stock = db.relationship('Stock', backref='client')
    
    
    def __repr__(self):
        return self.fullname

class Stock(db.Model, ModelMixin, SerializerMixin):
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete= 'CASCADE'), index=True)
    namestock = db.Column(db.String(100))
    nameproduct = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    sumquantity = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        return self.namestock

class Product(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-sales', '-comings', '-balances' )
    id = db.Column(db.Integer, primary_key=True)
    nameproduct = db.Column(db.String(200))
    sale = db.relationship('Sale', backref='product')
    coming = db.relationship('Coming', backref='product')
    balance = db.relationship('Balance', backref='product')
    
    def __repr__(self):
        return self.nameproduct, self.numberproduct

class Sale(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-product.sales', '-product.comings', '-product.balances', '-client.sales')
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete= 'CASCADE'), index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete= 'CASCADE'), index=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(11,2))
    sumprice = db.Column(db.Numeric(11,2))
    sumquantity = db.Column(db.Integer)
    status = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        return self.id

class Coming(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-product.id', '-product.sales', '-product.comings', '-product.balances',)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete= 'CASCADE'), index=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(11,2))
    sumquantity = db.Column(db.Integer)
    sumprice = db.Column(db.Numeric(11,2))
    comment = db.Column(db.Text)
    


    def __repr__(self):
        return str(self.id)

class Balance(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-product.id', '-product.sales', '-product.comings', '-product.balances',)
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete= 'CASCADE'), index=True)
    quantity = db.Column(db.Integer)
    current_quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(11,2))
    sumquantity = db.Column(db.Integer)
    sumprice = db.Column(db.Numeric(11,2))
    comment = db.Column(db.Text)

    def __repr__(self):
        return str(self.id)
