from app import db
from app.apibackend.resources.return_handlers import response_processing
from app.models import  Client
from flask import jsonify, request
from flask_restful import Resource


class ClientGetAll(Resource):
    def get(self):
        answer_code = '03'
        api_info = None
        clients_db = Client.query.all()
        if clients_db:
            answer_code = '00'
            api_info = [client_db.to_dict() for client_db in clients_db]
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ClientGetOne(Resource):
    def get(self, id):
        answer_code = '02'
        api_info = None
        client_db = Client.query.filter(Client.id == id).first()
        if client_db:
            answer_code = '00'         
            api_info = client_db.to_dict()        
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)


class ClientHandler(Resource):
    def post(self):
        answer_code = '04'
        api_info = None
        сlient_info_from_request = request.get_json()
        сlient_phone = сlient_info_from_request.get('phone')
        if not Client.query.filter(Client.phone == сlient_phone).first():
            answer_code = '01'
            client_db = Client(**сlient_info_from_request)
            client_db.save()
            api_info = Client.query.filter(Client.phone == сlient_phone).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def put(self):
        answer_code = '02'
        api_info = None
        client_info_from_request = request.get_json()
        client_id = client_info_from_request.get('id')
        client_db = Client.query.filter(Client.id == client_id).first()
        if client_id and client_db:
            answer_code = '05'
            client_info_from_request.pop('id', None)
            Client.query.filter(Client.id == client_id).update(client_info_from_request)
            db.session.commit()
            api_info = Client.query.filter(Client.id == client_id).first().to_dict()
        api_reply = response_processing(answer_code, api_info)
        return jsonify(api_reply)

    def delete(self):
        answer_code = '02'
        client_info_from_request = request.get_json()
        client_db = Client.query.filter(Client.id == client_info_from_request.get('id')).first()
        if client_db:
            answer_code = '00'         
            client_db.delete()        
        api_reply = response_processing(answer_code)
        return jsonify(api_reply)