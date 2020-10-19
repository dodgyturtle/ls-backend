from app import db
from app.models import Balance, Client, Coming, Product, Sale, Stock
from app.webbackend.forms import (AddClientForm, AddComingForm, AddProductForm,
                                  AddSaleForm, AddStockForm, DeleteForm,
                                  UpdateBalanceForm, UpdateClientForm,
                                  UpdateComingForm, UpdateProductForm,
                                  UpdateSaleForm, UpdateStockForm)
from app.webbackend.handlers import errors_convert_dict_to_string
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

web_blueprint = Blueprint('webbackend', __name__)


@web_blueprint.route('/product', methods=['GET', 'POST'])
@login_required
def product():
    form = AddProductForm(request.form)
    if form.validate_on_submit():
        product_db = Product(nameproduct=form.nameproduct.data, numberproduct=form.numberproduct.data)
        product_db.save()
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')
    products = Product.query.all()
    return render_template('webbackend/product.html', form=form, products=products)


@web_blueprint.route('/productupdate/<int:product_id>', methods=['GET', 'POST'])
@login_required
def productupdate(product_id: int):
    form =  UpdateProductForm(request.form)
    product_db = Product.query.filter(Product.id == product_id).first()
    if form.is_submitted():
        if form.submit.data and form.validate():
            Product.query.filter(Product.id == product_id).update(
                {
                    'nameproduct': form.nameproduct.data, 
                    'numberproduct': form.numberproduct.data
                }
            )
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.product'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.product'))
        else:
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')      
    return render_template('webbackend/productupdate.html', form=form, product=product_db)


@web_blueprint.route('/productdelete/<int:product_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
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
        flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')
    clients = Client.query.all()
    return render_template('webbackend/client.html', form=form, clients=clients)


@web_blueprint.route('/clientupdate/<int:client_id>', methods=['GET', 'POST'])
@login_required
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
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')      
    return render_template('webbackend/clientupdate.html', form=form, client=client_db)


@web_blueprint.route('/clientdelete/<int:client_id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def sale():
    form = AddSaleForm(request.form)
    form.client_id.choices = [(client.id, client.fullname) for client in Client.query.all()]
    form.product_id.choices = [(product.id, product.nameproduct) for product in Product.query.all()]
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
        if sale_db.id:
            balance_db = Balance.query.filter(Balance.product_id == sale_db.product_id).first()
        if balance_db:
            new_quantity = balance_db.quantity - sale_db.quantity
            new_sumprice = balance_db.price * float(new_quantity)
            Balance.query.filter(Balance.product_id == sale_db.product_id).update(
                {
                    'quantity': new_quantity,
                    'sumprice': new_sumprice,      
                }
            )
            db.session.commit() 
        else: 
            flash(f'Произошла ошибка обработки. База данных не доступна.', 'danger')
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')
    sales = Sale.query.all()
    return render_template('webbackend/sale.html', form=form, sales=sales)


@web_blueprint.route('/saleupdate/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def saleupdate(sale_id: int):
    form = UpdateSaleForm(request.form)
    form.client_id.choices = [(client.id, client.fullname) for client in Client.query.all()]
    form.product_id.choices = [(product.id, product.nameproduct) for product in Product.query.all()]
    sale_db = Sale.query.filter(Sale.id == sale_id).first()
    if form.is_submitted():
        if form.submit.data and form.validate():
            Sale.query.filter(Sale.id == sale_id).update(
                {
                    'client_id': form.client_id.data,
                    'product_id': form.product_id.data,
                    'quantity': form.quantity.data,
                    'price': form.price.data,
                    'sumprice': form.sumprice.data,
                    'status': form.status.data,
                    'comment': form.comment.data,
                }
            )
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.sale'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.sale'))
        else:
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger') 
    return render_template('webbackend/saleupdate.html', form=form, sale=sale_db)


@web_blueprint.route('/saledelete/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def saledelete(sale_id: int):
    form =  DeleteForm(request.form)
    sale_db = Sale.query.filter(Sale.id == sale_id).first()
    if form.is_submitted():
        if form.submit.data and sale_db:      
            sale_db.delete()
            flash('Удалено!', 'info')
            return redirect(url_for('webbackend.sale'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.sale'))  
    return render_template('webbackend/saledelete.html', form=form, sale=sale_db)


@web_blueprint.route('/coming', methods=['GET', 'POST'])
@login_required
def coming():
    form = AddComingForm(request.form)
    form.product_id.choices = [(product.id, product.nameproduct) for product in Product.query.all()]
    if form.validate_on_submit():
        coming_db = Coming(
            product_id = form.product_id.data,
            quantity = form.quantity.data,
            price = form.price.data,
            sumprice = form.sumprice.data,
            comment = form.comment.data,
        )
        coming_db.save()
        if coming_db.id:
            balance_db = Balance.query.filter(Balance.product_id == coming_db.product_id).first()
        if balance_db:
            new_quantity = balance_db.quantity + coming_db.quantity
            new_price = coming_db.price
            new_sumprice = new_price * float(new_quantity)
            Balance.query.filter(Balance.product_id == coming_db.product_id).update(
                {
                    'quantity': new_quantity,
                    'price': new_price,
                    'sumprice': new_sumprice,      
                }
            )
            db.session.commit()         
        else:
            balance_db=Balance(
                product_id = form.product_id.data,
                quantity = form.quantity.data,
                price = form.price.data,
                sumprice = form.sumprice.data,
                comment = form.comment.data,
            )
            balance_db.save()
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')
    comings = Coming.query.all()
    return render_template('webbackend/coming.html', form=form, comings=comings)


@web_blueprint.route('/comingupdate/<int:coming_id>', methods=['GET', 'POST'])
@login_required
def comingupdate(coming_id: int):
    form =  UpdateComingForm(request.form)
    coming_db = Coming.query.filter(Coming.id == coming_id).first()
    form.product_id.choices = [(product.id, product.nameproduct) for product in Product.query.all()]
    if form.is_submitted():
        if form.submit.data and form.validate():
            Coming.query.filter(Coming.id == coming_id).update(
                {
                    'product_id': form.product_id.data,
                    'quantity': form.quantity.data,
                    'price': form.price.data,
                    'sumprice': form.sumprice.data,
                    'comment': form.comment.data,
                }
            )
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.coming'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.coming'))
        else:
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')      
    return render_template('webbackend/comingupdate.html', form=form, coming=coming_db)


@web_blueprint.route('/comingdelete/<int:coming_id>', methods=['GET', 'POST'])
@login_required
def comingdelete(coming_id: int):
    form =  DeleteForm(request.form)
    coming_db = Coming.query.filter(Coming.id == coming_id).first()
    if form.is_submitted():
        if form.submit.data and coming_db:      
            coming_db.delete()
            flash('Удалено!', 'info')
            return redirect(url_for('webbackend.coming'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.coming'))  
    return render_template('webbackend/comingdelete.html', form=form, coming=coming_db)


@web_blueprint.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    balances = Balance.query.all()
    return render_template('webbackend/balance.html', balances=balances)


@web_blueprint.route('/balanceupdate/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def balanceupdate(balance_id: int):
    form =  UpdateBalanceForm(request.form)
    balance_db = Balance.query.filter(Balance.id == balance_id).first()
    form.product_id.choices = [(product.id, product.nameproduct) for product in Product.query.all()]
    if form.is_submitted():
        if form.submit.data and form.validate():
            Balance.query.filter(Balance.id == balance_id).update(
                {
                    'product_id': form.product_id.data,
                    'quantity': form.quantity.data,
                    'price': form.price.data,
                    'sumprice': form.sumprice.data,
                }
            )
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.balance'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.balance'))
        else:
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')      
    return render_template('webbackend/balanceupdate.html', form=form, balance=balance_db)


@web_blueprint.route('/balancedelete/<int:balance_id>', methods=['GET', 'POST'])
@login_required
def balancedelete(balance_id: int):
    form =  DeleteForm(request.form)
    balance_db = Balance.query.filter(Balance.id == balance_id).first()
    if form.is_submitted():
        if form.submit.data and balance_db:      
            balance_db.delete()
            flash('Удалено!', 'info')
            return redirect(url_for('webbackend.balance'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.balance'))  
        else:
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')
    return render_template('webbackend/balancedelete.html', form=form, balance=balance_db)


@web_blueprint.route('/stock', methods=['GET', 'POST'])
@login_required
def stock():
    form = AddStockForm(request.form)
    if form.validate_on_submit():
        stock_db = Stock(
            namestock =  form.namestock.data,
            nameproduct = form.nameproduct.data,
            quantity = form.quantity.data,
            comment = form.comment.data,
        )
        stock_db.save()
    elif form.is_submitted():
        flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')
    stocks = Stock.query.all()
    return render_template('webbackend/stock/stock.html', form=form, stocks=stocks)


@web_blueprint.route('/stockupdate/<int:stock_id>', methods=['GET', 'POST'])
def stockupdate(stock_id: int):
    form =  UpdateStockForm(request.form)
    stock_db = Stock.query.filter(Stock.id == stock_id).first()
    if form.is_submitted():
        if form.submit.data and form.validate():
            Stock.query.filter(Stock.id == stock_id).update(
                {
                    'namestock': form.namestock.data,
                    'nameproduct': form.nameproduct.data,
                    'quantity': form.quantity.data,
                    'comment': form.comment.data,
                }
            )
            db.session.commit()
            flash('Обновлено!', 'info')
            return redirect(url_for('webbackend.stock'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.stock'))
        else:
            flash(f'Ошибка ввода данных: { errors_convert_dict_to_string(form.errors) }', 'danger')      
    return render_template('webbackend/stock/stockupdate.html', form=form, stock=stock_db)


@web_blueprint.route('/stockdelete/<int:stock_id>', methods=['GET', 'POST'])
@login_required
def stockdelete(stock_id: int):
    form =  DeleteForm(request.form)
    stock_db = Stock.query.filter(Stock.id == stock_id).first()
    if form.is_submitted():
        if form.submit.data and stock_db:      
            stock_db.delete()
            flash('Удалено!', 'info')
            return redirect(url_for('webbackend.stock'))  
        elif form.cancel.data:
            return redirect(url_for('webbackend.stock'))  
    return render_template('webbackend/stock/stockdelete.html', form=form, stock=stock_db)

@web_blueprint.route('/order/<int:client_id>', methods=['GET', 'POST'])
@login_required
def order(client_id: int):
    orders_db = Sale.query.filter(Sale.client_id == client_id).all()
    return render_template('webbackend/order/order.html', orders=orders_db)