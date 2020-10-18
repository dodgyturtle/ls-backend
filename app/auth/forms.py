from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo

from .models import User


class LoginForm(FlaskForm):
    user_id = StringField('Пользователь', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired(), Length(2, 30)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(3, 30)])
    password_confirmation = PasswordField(
        'Подтвердите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли не совпадают.')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError('Такой пользователь уже существует')