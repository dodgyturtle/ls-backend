from app import db
from app.apibackend.resources.return_handlers import response_processing
from app.models import  Coming
from flask import jsonify, request
from flask_restful import Resource


class ComingGetAll(Resource):
    def get(self):
        answer_code = '18'
        api_info = None
        all_coming_db = Coming.query.all()
        if all_coming_db:
            answer_code = '00'
            api_info = [coming_db.to_dict() for coming_db in all_coming_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ComingGetOne(Resource):
    def get(self, id):
        answer_code = '17'
        api_info = None
        coming_db = Coming.query.filter(Coming.id == id).first()
        print(coming_db.to_dict())
        if coming_db:
            answer_code = '00'         
            api_info = coming_db.to_dict()        
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ComingHandler(Resource):
    def post(self):
        answer_code = '16'
        сoming_info_from_request = request.get_json()
        сoming_db = Coming(**сoming_info_from_request)
        сoming_db.save()
        api_info = сoming_db.to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        answer_code = '17'
        api_info = None
        сoming_info_from_request = request.get_json()
        сoming_id = сoming_info_from_request.get('id')
        сoming_db = Coming.query.filter(Coming.id == сoming_id).first()
        if сoming_id and сoming_db:
            answer_code = '20'
            сoming_info_from_request.pop('id', None)
            Coming.query.filter(Coming.id == сoming_id).update(сoming_info_from_request)
            db.session.commit()
            api_info = Coming.query.filter(Coming.id == сoming_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        answer_code = '17'
        сoming_info_from_request = request.get_json()
        сoming_db = Coming.query.filter(Coming.id == сoming_info_from_request.get('id')).first()
        if сoming_db:
            answer_code = '00'         
            сoming_db.delete()        
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)