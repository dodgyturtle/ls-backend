import datetime
from sqlalchemy_serializer import SerializerMixin

from app import db
from app.utils import ModelMixin

from app.auth.models import AnonymousUser, User


class Client(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-sales', '-comings', '-balances' )
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, unique=True)
    productname = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    comment = db.Column(db.Text)
    
    def __repr__(self):
        return self.fullname

class Stock(db.Model, ModelMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    namestock = db.Column(db.String(100))
    nameproduct = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    date = db.Column(db.String, default=datetime.datetime.utcnow().strftime('%d-%m-%Y'))
    comment = db.Column(db.Text)
    sumquantity = db.Column(db.Integer)

    def __repr__(self):
        return self.namestock

class Product(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-sales', '-comings', '-balances' )
    id = db.Column(db.Integer, primary_key=True)
    nameproduct = db.Column(db.String(100))
    numberproduct = db.Column(db.String(100))
    
    def __repr__(self):
        return self.nameproduct, self.numberproduct

class Sale(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-product.sales', '-product.comings', '-product.balances', '-client.sales')
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete= 'CASCADE'), index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id', ondelete= 'CASCADE'), index=True)
    price = db.Column(db.Float)
    quantuty = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    comment = db.Column(db.Text)
    status = db.Column(db.Boolean, default=True)
    sumprice = db.Column(db.Float)
    sumquantity = db.Column(db.Integer)
    product = db.relationship('Product', backref='sales')
    client = db.relationship('Client', backref='sales')

    def __repr__(self):
        return self.id

class Coming(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-product.id', '-product.sales', '-product.comings', '-product.balances',)
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete= 'CASCADE'), index=True)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    date = db.Column(db.String, default=datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M'))
    comment = db.Column(db.Text)
    sumprice = db.Column(db.Float)
    sumquantity = db.Column(db.Integer)
    product = db.relationship('Product', backref='comings')


    def __repr__(self):
        return str(self.id)

class Balance(db.Model, ModelMixin, SerializerMixin):
    serialize_rules = ('-product.id', '-product.sales', '-product.comings', '-product.balances',)
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete= 'CASCADE'), index=True)
    price = db.Column(db.Float)
    quantuty = db.Column(db.Integer)
    date = db.Column(db.String, default=datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M'))
    comment = db.Column(db.Text)
    sumprice = db.Column(db.Float)
    sumquantity = db.Column(db.Integer)
    product = db.relationship('Product', backref='balances')

    def __repr__(self):
        return str(self.id)