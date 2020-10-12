from app import db
from app.apibackend.resources.return_handlers import response_processing
from app.models import  Product
from flask import jsonify, request
from flask_restful import Resource


class ProductGetAll(Resource):
    def get(self):
        answer_code = '13'
        api_info = None
        all_product_db = Product.query.all()
        if all_product_db:
            answer_code = '00'
            api_info = [product_db.to_dict() for product_db in all_product_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ProductGetOne(Resource):
    def get(self, id):
        answer_code = '12'
        api_info = None
        product_db = Product.query.filter(Product.id == id).first()
        if product_db:
            answer_code = '00'         
            api_info = product_db.to_dict()        
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ProductHandler(Resource):
    def post(self):
        answer_code = '11'
        product_info_from_request = request.get_json()
        product_db = Product(**product_info_from_request)
        product_db.save()
        api_info = product_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        answer_code = '12'
        api_info = None
        product_info_from_request = request.get_json()
        product_id = product_info_from_request.get('id')
        product_db = Product.query.filter(Product.id == product_id).first()
        if product_id and product_db:
            answer_code = '15'
            product_info_from_request.pop('id', None)
            Product.query.filter(Product.id == product_id).update(product_info_from_request)
            db.session.commit()
            api_info = Product.query.filter(Product.id == product_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        answer_code = '12'
        product_info_from_request = request.get_json()
        product_db = Product.query.filter(Product.id == product_info_from_request.get('id')).first()
        if product_db:
            answer_code = '00'         
            product_db.delete()        
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)