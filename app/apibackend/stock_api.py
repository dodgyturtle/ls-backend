from app import db
from app.apibackend.resources.return_handlers import (
    response_processing,
    checking_existence_in_db,
)
from app.models import Stock, Client
from flask import jsonify, request
from flask_restful import Resource


class StockGetAll(Resource):
    def get(self):
        """Get all stocks.
        :param:
        :return:
        """
        answer_code = "08"
        api_info = None
        all_stock_db = Stock.query.all()
        if all_stock_db:
            answer_code = "00"
            api_info = [stock_db.to_dict() for stock_db in all_stock_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class StockGetOne(Resource):
    def get(self, id):
        """Get one stock.
        :param: id
        :return:
        """
        answer_code = "07"
        api_info = None
        stock_db = Stock.query.filter(Stock.id == id).first()
        if stock_db:
            answer_code = "00"
            api_info = stock_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class StockHandler(Resource):
    def post(self):
        """Add stock.
        :param:
        :return:
        """
        answer_code = "02"
        api_info = None
        stock_info_from_request = request.get_json()
        if checking_existence_in_db(Client, stock_info_from_request.get("client_id")):
            answer_code = "06"
            stock_db = Stock(**stock_info_from_request)
            stock_db.save()
            api_info = stock_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        """Update stock.
        :param: id
        :return:
        """
        answer_code = "07"
        api_info = None
        stock_info_from_request = request.get_json()
        stock_id = stock_info_from_request.get("id")
        stock_db = Stock.query.filter(Stock.id == stock_id).first()
        if stock_id and stock_db:
            answer_code = "10"
            stock_info_from_request.pop("id", None)
            Stock.query.filter(Stock.id == stock_id).update(stock_info_from_request)
            db.session.commit()
            api_info = Stock.query.filter(Stock.id == stock_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        """Delete stock.
        :param: id
        :return:
        """
        answer_code = "07"
        stock_info_from_request = request.get_json()
        stock_db = Stock.query.filter(
            Stock.id == stock_info_from_request.get("id")
        ).first()
        if stock_db:
            answer_code = "00"
            stock_db.delete()
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)