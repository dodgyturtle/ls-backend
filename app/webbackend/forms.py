from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from app.models import Client, Stock, Product, Coming, Sale, Balance


class AddProductForm(FlaskForm):
    productname = StringField('Название', [DataRequired()])
    productnumber = StringField('Модель', [DataRequired()])
    submit = SubmitField('Добавить')
    
    def validate_product(form, field):
        if (Product.query.filter_by(productname=field.productname).first() is not None) or (
            Product.query.filter_by(productnumber=field.productnumber).first() is not None):
            raise ValidationError('Продукт существует')
     


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 30)])
    password_confirmation = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password do not match.')])
    submit = SubmitField('Register')

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('This username is taken.')