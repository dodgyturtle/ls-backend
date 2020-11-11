from app import db
from decimal import Decimal
from app.apibackend.resources.return_handlers import (
    response_processing,
    checking_existence_in_db,
)
from app.models import Sale, Product, Client, Balance
from flask import jsonify, request
from flask_restful import Resource


class SaleGetAll(Resource):
    def get(self):
        """Get all sales.
        :param:
        :return:
        """
        answer_code = "23"
        api_info = None
        all_sale_db = Sale.query.all()
        if all_sale_db:
            answer_code = "00"
            api_info = [sale_db.to_dict() for sale_db in all_sale_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class SaleGetOne(Resource):
    def get(self, id):
        """Get one sale.
        :param: id
        :return:
        """
        answer_code = "22"
        api_info = None
        sale_db = Sale.query.filter(Sale.id == id).first()
        if sale_db:
            answer_code = "00"
            api_info = sale_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class SaleHandler(Resource):
    def post(self):
        """Add sale.
        :param:
        :return:
        """
        answer_code = "31"
        api_info = None
        sale_info_from_request = request.get_json()
        if checking_existence_in_db(
            Client, sale_info_from_request.get("client_id")
        ) and checking_existence_in_db(
            Product, sale_info_from_request.get("product_id")
        ):
            sale_db = Sale(**sale_info_from_request)
            sale_db.save()
            if sale_db.id:
                balance_db = Balance.query.filter(
                    Balance.product_id == sale_db.product_id
                ).first()
            if balance_db:
                answer_code = "21"
                new_quantity = balance_db.current_quantity - sale_db.quantity
                new_sumprice = balance_db.price * Decimal(new_quantity)
                Balance.query.filter(Balance.product_id == sale_db.product_id).update(
                    {
                        "current_quantity": new_quantity,
                        "sumprice": new_sumprice,
                    }
                )
                db.session.commit()
                api_info = sale_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        """Update sale.
        :param:
        :return:
        """
        answer_code = "22"
        api_info = None
        sale_info_from_request = request.get_json()
        sale_id = sale_info_from_request.get("id")
        sale_db = Sale.query.filter(Sale.id == sale_id).first()
        if sale_id and sale_db:
            answer_code = "25"
            sale_info_from_request.pop("id", None)
            Sale.query.filter(Sale.id == sale_id).update(sale_info_from_request)
            db.session.commit()
            api_info = Sale.query.filter(Sale.id == sale_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        """Delete sale.
        :param:
        :return:
        """
        answer_code = "22"
        sale_info_from_request = request.get_json()
        sale_db = Sale.query.filter(Sale.id == sale_info_from_request.get("id")).first()
        if sale_db:
            answer_code = "00"
            sale_db.delete()
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)