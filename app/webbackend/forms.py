from app.models import Balance, Client, Coming, Product, Sale, Stock
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, FloatField, IntegerField,
                     SelectField, StringField, SubmitField, ValidationError)
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange


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
    phone = IntegerField('Номер телефона', [DataRequired(), NumberRange(min=89000000000, max=89999999999, message = "Введите номер телефона начиная с '8', без пробелов и символов '+' и '-'.")])
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

    client_id = SelectField("Клиент", coerce=int)
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество")
    price = FloatField("Стоимость")
    sumprice = FloatField("Итогова сумма")
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Добавить')

    def validate_quantity(form, field):
        balance_quantity = Balance.query.filter_by(product_id=form.product_id.data).first().quantity
        if balance_quantity < form.quantity.data:
            raise ValidationError('Данный товар отсутствует на складе в таком количестве.')

class UpdateSaleForm(FlaskForm):

    client_id = SelectField("Клиент", coerce=int)
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество")
    price = FloatField("Стоимость")
    sumprice = FloatField("Итогова сумма")
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')

    def validate_quantity(form, field):
        balance_quantity = Balance.query.filter_by(product_id=form.product_id.data).first().quantity
        if balance_quantity < form.quantity.data:
            raise ValidationError('Данный товар отсутствует на складе в таком количестве.')

class AddComingForm(FlaskForm):

    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество")
    price = FloatField("Стоимость")
    sumquantity = IntegerField("Итоговое количество")
    sumprice = FloatField("Итогова сумма")
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Добавить')

class UpdateComingForm(FlaskForm):

    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество")
    price = FloatField("Стоимость")
    sumprice = FloatField("Итогова сумма")
    comment = StringField('Комментарий', [Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')

class UpdateBalanceForm(FlaskForm):
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество")
    price = FloatField("Стоимость")
    sumprice = FloatField("Итогова сумма")
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')

class AddStockForm(FlaskForm):
    namestock = StringField('Название акции', [Length(0, 200)])
    nameproduct = StringField('Наименование товара', [Length(0, 200)])
    quantity = IntegerField("Количество")
    comment = StringField('Комментарий', [Length(0, 200)])
    submit = SubmitField('Добавить')
    

class UpdateStockForm(FlaskForm):
    namestock = StringField('Название акции', [Length(0, 200)])
    nameproduct = StringField('Наименование товара', [Length(0, 200)])
    quantity = IntegerField("Количество")
    comment = StringField('Комментарий', [Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')

