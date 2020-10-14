from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, IntegerField, SelectField, BooleanField, FloatField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

from app.models import Client, Stock, Product, Coming, Sale, Balance

from wtforms.fields.html5 import TelField

class AddProductForm(FlaskForm):
    nameproduct = StringField('Название', [DataRequired()])
    numberproduct = StringField('Модель ', [DataRequired()])
    submit = SubmitField('Добавить')
    
    def validate_numberproduct(form, field):
        if Product.query.filter_by(numberproduct=field.data).first() is not None:
            raise ValidationError('Такая модель товара существует.') 

class UpdateProductForm(FlaskForm):
    id = StringField('Id')
    nameproduct = StringField('Название')
    numberproduct = StringField('Модель')
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')

    def validate_numberproduct(form, field):
        if Product.query.filter_by(numberproduct=field.data).first() is not None:
            raise ValidationError('Такая модель товара существует.') 

class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить')
    cancel = SubmitField('Отменить')


class AddClientForm(FlaskForm):
    fullname = StringField('ФИО')
    phone = IntegerField('Номер телефона', [DataRequired()])
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Добавить')
    
    def validate_phone(form, field):
        if Client.query.filter_by(phone=field.data).first() is not None:
            raise ValidationError('Такой клиент существует.')

class UpdateClientForm(FlaskForm):
    fullname = StringField('ФИО')
    phone = IntegerField('Номер телефона', [DataRequired(), NumberRange(min=89000000000, max=89999999999, message = "Введите номер телефона начиная с '8', без пробелов и символов '+' и '-'.")])
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')

class AddSaleForm(FlaskForm):
    
    clients = Client.query.all()
    products = Product.query.all()

    client_id = SelectField("Клиент", choices=clients)
    product_id = SelectField("Товар", choices=products)
    quantity = IntegerField("Количество")
    price = FloatField("Стоимость")
    comment = StringField('Комментарий',[Length(0, 200)])
    sumprice = FloatField("Итогова сумма")
    status = BooleanField('Статус')
    date = DateTimeField("Дата и Время")
    submit = SubmitField('Добавить')
