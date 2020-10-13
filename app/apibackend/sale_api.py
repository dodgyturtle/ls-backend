from app import db
from app.apibackend.resources.return_handlers import response_processing
from app.models import  Sale
from flask import jsonify, request
from flask_restful import Resource


class SaleGetAll(Resource):
    def get(self):
        answer_code = '23'
        api_info = None
        all_sale_db = Sale.query.all()
        if all_sale_db:
            answer_code = '00'
            api_info = [sale_db.to_dict() for sale_db in all_sale_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class SaleGetOne(Resource):
    def get(self, id):
        answer_code = '22'
        api_info = None
        sale_db = Sale.query.filter(Sale.id == id).first()
        if sale_db:
            answer_code = '00'         
            api_info = sale_db.to_dict()        
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class SaleHandler(Resource):
    def post(self):
        answer_code = '21'
        sale_info_from_request = request.get_json()
        sale_db = Sale(**sale_info_from_request)
        sale_db.save()
        api_info = sale_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        answer_code = '22'
        api_info = None
        sale_info_from_request = request.get_json()
        sale_id = sale_info_from_request.get('id')
        sale_db = Sale.query.filter(Sale.id == sale_id).first()
        if sale_id and sale_db:
            answer_code = '25'
            sale_info_from_request.pop('id', None)
            Sale.query.filter(Sale.id == sale_id).update(sale_info_from_request)
            db.session.commit()
            api_info = Sale.query.filter(sale.id == sale_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        answer_code = '22'
        sale_info_from_request = request.get_json()
        sale_db = Sale.query.filter(Sale.id == sale_info_from_request.get('id')).first()
        if sale_db:
            answer_code = '00'         
            sale_db.delete()        
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)