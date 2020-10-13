from app import db
from app.apibackend.resources.return_handlers import response_processing
from app.models import  Balance
from flask import jsonify, request
from flask_restful import Resource


class BalanceGetAll(Resource):
    def get(self):
        answer_code = '28'
        api_info = None
        all_balance_db = Balance.query.all()
        if all_balance_db:
            answer_code = '00'
            api_info = [balance_db.to_dict() for balance_db in all_balance_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class BalanceGetOne(Resource):
    def get(self, id):
        answer_code = '27'
        api_info = None
        balance_db = Balance.query.filter(Balance.id == id).first()
        if balance_db:
            answer_code = '00'         
            api_info = balance_db.to_dict()        
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class BalanceHandler(Resource):
    def post(self):
        answer_code = '26'
        balance_info_from_request = request.get_json()
        balance_db = Balance(**balance_info_from_request)
        balance_db.save()
        api_info = balance_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        answer_code = '27'
        api_info = None
        balance_info_from_request = request.get_json()
        balance_id = balance_info_from_request.get('id')
        balance_db = Balance.query.filter(Balance.id == balance_id).first()
        if balance_id and balance_db:
            answer_code = '30'
            balance_info_from_request.pop('id', None)
            Balance.query.filter(Balance.id == balance_id).update(balance_info_from_request)
            db.session.commit()
            api_info = Balance.query.filter(Balance.id == balance_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        answer_code = '27'
        balance_info_from_request = request.get_json()
        balance_db = Balance.query.filter(Balance.id == balance_info_from_request.get('id')).first()
        if balance_db:
            answer_code = '00'         
            balance_db.delete()        
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)