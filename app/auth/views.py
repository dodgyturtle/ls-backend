from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.auth.models import User
from app.auth.forms import LoginForm, RegistrationForm

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        user.save()
        login_user(user)
        flash('Вы зарегистрированы!', 'success')
        return redirect(url_for("webbackend.sale"))
    elif form.is_submitted():
        flash('Ошибка ввода данных!', 'danger')
    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if current_user.is_authenticated:
	    return redirect(url_for('webbackend.sale'))
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash('Успешная авторизация', 'success')
            return redirect(url_for('webbackend.sale'))
        flash('Неверный пользователь или пароль', 'danger')
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли.', 'info')
    return redirect(url_for('main.index'))

@auth_blueprint.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    users = User.query.all()
    return render_template('auth/users.html', users=users)


