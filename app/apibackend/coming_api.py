from app import db
from decimal import Decimal
from app.apibackend.resources.return_handlers import (
    response_processing,
    checking_existence_in_db,
)
from app.models import Coming, Product, Balance
from flask import jsonify, request
from flask_restful import Resource


class ComingGetAll(Resource):
    def get(self):
        """Get all comings.
        :param:
        :return:
        """
        answer_code = "18"
        api_info = None
        all_coming_db = Coming.query.all()
        if all_coming_db:
            answer_code = "00"
            api_info = [coming_db.to_dict() for coming_db in all_coming_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ComingGetOne(Resource):
    def get(self, id):
        """Get one coming.
        :param: id
        :return:
        """
        answer_code = "17"
        api_info = None
        coming_db = Coming.query.filter(Coming.id == id).first()
        if coming_db:
            answer_code = "00"
            api_info = coming_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ComingHandler(Resource):
    def post(self):
        """Add coming.
        :param:
        :return:
        """
        answer_code = "12"
        api_info = None
        coming_info_from_request = request.get_json()
        if checking_existence_in_db(
            Product, coming_info_from_request.get("product_id")
        ):
            answer_code = "16"
            coming_db = Coming(**coming_info_from_request)
            coming_db.save()
            if coming_db.id:
                balance_db = Balance.query.filter(
                    Balance.product_id == coming_db.product_id
                ).first()
            if balance_db:
                new_quantity = balance_db.current_quantity + coming_db.quantity
                new_price = coming_db.price
                new_sumprice = new_price * Decimal(new_quantity)
                Balance.query.filter(Balance.product_id == coming_db.product_id).update(
                    {
                        "quantity": new_quantity,
                        "current_quantity": new_quantity,
                        "price": new_price,
                        "sumprice": new_sumprice,
                    }
                )
                db.session.commit()
            else:
                balance_db = Balance(
                    product_id=coming_db.product_id,
                    quantity=coming_db.quantity,
                    current_quantity=coming_db.quantity,
                    price=coming_db.price,
                    sumprice=coming_db.sumprice,
                    comment=coming_db.comment,
                )
                balance_db.save()
            api_info = coming_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        """Update coming.
        :param: id
        :return:
        """
        answer_code = "17"
        api_info = None
        coming_info_from_request = request.get_json()
        coming_id = coming_info_from_request.get("id")
        coming_db = Coming.query.filter(Coming.id == coming_id).first()
        if coming_db:
            answer_code = "20"
            coming_info_from_request.pop("id", None)
            Coming.query.filter(Coming.id == coming_id).update(coming_info_from_request)
            db.session.commit()
            api_info = Coming.query.filter(Coming.id == coming_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        """Delete coming.
        :param: id
        :return:
        """
        answer_code = "17"
        coming_info_from_request = request.get_json()
        coming_db = Coming.query.filter(
            Coming.id == coming_info_from_request.get("id")
        ).first()
        if coming_db:
            answer_code = "00"
            coming_db.delete()
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)