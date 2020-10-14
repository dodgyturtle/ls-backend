from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required

from app import db
from app.models import Product, Client, Sale
from app.webbackend.forms import AddProductForm, DeleteForm, UpdateProductForm, AddClientForm, UpdateClientForm, AddSaleForm

web_blueprint = Blueprint('webbackend', __name__)


@web_blueprint.route('/product', methods=['GET', 'POST'])
def product():
    form = AddProductForm(request.form)
    if form.validate_on_submit():
        product_db = Product(nameproduct=form.nameproduct.data, numberproduct=form.numberproduct.data)
        product_db.save()
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: { ", ".join(form.errors.get("nameproduct") or form.errors.get("numberproduct"))}', 'danger')
    products = Product.query.all()
    return render_template('webbackend/product.html', form=form, products=products)


@web_blueprint.route('/productupdate/<int:product_id>', methods=['GET', 'POST'])
def productupdate(product_id: int):
    form =  UpdateProductForm(request.form)
    product_db = Product.query.filter(Product.id == product_id).first()
    if form.is_submitted():
        if form.submit.data and form.validate():
            Product.query.filter(Product.id == product_id).update({'nameproduct': form.nameproduct.data, 'numberproduct': form.numberproduct.data})
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.product'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.product'))
        else:
            flash(f'Ошибка ввода данных: { ", ".join(form.errors.get("nameproduct") or form.errors.get("numberproduct"))}', 'danger')      
    return render_template('webbackend/productupdate.html', form=form, product=product_db)


@web_blueprint.route('/productdelete/<int:product_id>', methods=['GET', 'POST'])
def productdelete(product_id: int):
    form =  DeleteForm(request.form)
    product_db = Product.query.filter(Product.id == product_id).first()
    if form.is_submitted():
        if form.submit.data and product_db:      
            product_db.delete()
            flash('Удалено!', 'info')
            return redirect(url_for('webbackend.product'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.product'))  
    return render_template('webbackend/productdelete.html', form=form, product=product_db)


@web_blueprint.route('/client', methods=['GET', 'POST'])
def client():
    form = AddClientForm(request.form)
    if form.validate_on_submit():
        client_db = Client(
            fullname =  form.fullname.data,
            phone = form.phone.data,
            status = form.status.data,
            comment = form.comment.data,
        )
        client_db.save()
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: { ", ".join(form.errors.get("phone"))}', 'danger')
    clients = Client.query.all()
    return render_template('webbackend/client.html', form=form, clients=clients)


@web_blueprint.route('/clientupdate/<int:client_id>', methods=['GET', 'POST'])
def clientupdate(client_id: int):
    form =  UpdateClientForm(request.form)
    client_db = Client.query.filter(Client.id == client_id).first()
    if form.is_submitted():
        if form.submit.data and form.validate():
            Client.query.filter(Client.id == client_id).update(
                {
                    'fullname': form.fullname.data,
                    'phone': form.phone.data,
                    'status': form.status.data,
                    'comment': form.comment.data,
                }
            )
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.client'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.client'))
        else:
            flash(f'Ошибка ввода данных: { ", ".join(form.errors.get("phone"))}', 'danger')      
    return render_template('webbackend/clientupdate.html', form=form, client=client_db)


@web_blueprint.route('/clientdelete/<int:client_id>', methods=['GET', 'POST'])
def clientdelete(client_id: int):
    form =  DeleteForm(request.form)
    client_db = Client.query.filter(Client.id == client_id).first()
    if form.is_submitted():
        if form.submit.data and client_db:      
            client_db.delete()
            flash('Удалено!', 'info')
            return redirect(url_for('webbackend.client'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.client'))  
    return render_template('webbackend/clientdelete.html', form=form, client=client_db)


@web_blueprint.route('/sale', methods=['GET', 'POST'])
def sale():
    form = AddSaleForm(request.form)
    if form.validate_on_submit():
        sale_db = Sale(
            client_id = form.client_id.data,
            product_id = form.product_id.data,
            quantity = form.quantity.data,
            price = form.price.data,
            comment = form.comment.data,
            sumprice = form.sumprice.data,
            status = form.status.data,
        )
        sale_db.save()
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: {form.errors }', 'danger')
    sales = Sale.query.all()
    return render_template('webbackend/sale.html', form=form, sales=sales)