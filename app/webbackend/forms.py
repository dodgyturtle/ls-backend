from app.models import Balance, Client, Coming, Product, Sale, Stock
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, DecimalField, IntegerField,
                     SelectField, StringField, SubmitField, ValidationError)
from wtforms.validators import (DataRequired, EqualTo, Length, NumberRange,
                                Optional)


class AddProductForm(FlaskForm):
    nameproduct = StringField('Название', [DataRequired()])
    submit = SubmitField('Добавить')
        
    def validate_nameproduct(form, field):
        if Product.query.filter_by(nameproduct=field.data).first() is not None:
            raise ValidationError('Такой товар существует.')
    
    
class UpdateProductForm(FlaskForm):
    id = StringField('Id')
    nameproduct = StringField('Название', [DataRequired()])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')
    
    def validate_nameproduct(form, field):
        if Product.query.filter_by(nameproduct=field.data).first() is not None:
            raise ValidationError('Такой товар существует.')


class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить')
    cancel = SubmitField('Отменить')


class AddClientForm(FlaskForm):
    fullname = StringField('ФИО')
    phone = IntegerField('Номер телефона', [Optional()])
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Добавить')
    
    def validate_phone(form, field):
        if Client.query.filter_by(phone=field.data).first() is not None:
            raise ValidationError('Такой клиент существует.')


class UpdateClientForm(FlaskForm):
    fullname = StringField('ФИО')
    phone = IntegerField('Номер телефона', [Optional()])
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')


class AddSaleForm(FlaskForm):
    client_id = SelectField("Клиент", coerce=int)
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество", [DataRequired(), Optional()])
    price = DecimalField("Стоимость", [DataRequired(), Optional()])
    sumprice = DecimalField("Итогова сумма", [Optional()])
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
    quantity = IntegerField("Количество", [DataRequired(), Optional()])
    price = DecimalField("Стоимость", [DataRequired(), Optional()])
    sumprice = DecimalField("Итогова сумма", [Optional()])
    status = BooleanField('Статус')
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')


class AddComingForm(FlaskForm):
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество", [DataRequired(), Optional()])
    price = DecimalField("Стоимость", [DataRequired(), Optional()])
    sumquantity = IntegerField("Итоговое количество", [Optional()])
    sumprice = DecimalField("Итогова сумма")
    comment = StringField('Комментарий',[Length(0, 200)])
    submit = SubmitField('Добавить')


class UpdateComingForm(FlaskForm):
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество", [DataRequired(), Optional()])
    price = DecimalField("Стоимость", [DataRequired(), Optional()])
    sumprice = DecimalField("Итогова сумма", [Optional()])
    comment = StringField('Комментарий', [Length(0, 200)])
    submit = SubmitField('Изменить')
    cancel = SubmitField('Отменить')


class UpdateBalanceForm(FlaskForm):
    product_id = SelectField("Товар", coerce=int)
    quantity = IntegerField("Количество", [DataRequired(), Optional()])
    price = DecimalField("Стоимость", [DataRequired(), Optional()])
    sumprice = DecimalField("Итогова сумма", [Optional()])
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

