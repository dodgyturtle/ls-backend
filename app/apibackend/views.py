from app import api, db
from flask import Blueprint


from app.apibackend.client_api import ClientGetAll, ClientGetOne, ClientHandler
from app.apibackend.stock_api import StockGetAll, StockGetOne, StockHandler
from app.apibackend.product_api import ProductGetAll, ProductGetOne, ProductHandler
from app.apibackend.coming_api import ComingGetAll, ComingGetOne, ComingHandler
from app.apibackend.sale_api import SaleGetAll, SaleGetOne, SaleHandler
from app.apibackend.balance_api import BalanceGetAll, BalanceGetOne, BalanceHandler 

api_blueprint = Blueprint('apibackend', __name__)

#Client
api.add_resource(ClientGetAll, '/api/v1/clientgetall')
api.add_resource(ClientGetOne, '/api/v1/clientgetone/<id>')
api.add_resource(ClientHandler, '/api/v1/clienthandler')

#Stock
api.add_resource(StockGetAll , '/api/v1/stockgetall')
api.add_resource(StockGetOne, '/api/v1/stockgetone/<id>')
api.add_resource(StockHandler, '/api/v1/stockhandler')

#Product
api.add_resource(ProductGetAll , '/api/v1/productgetall')
api.add_resource(ProductGetOne, '/api/v1/productgetone/<id>')
api.add_resource(ProductHandler, '/api/v1/producthandler')

#Coming
api.add_resource(ComingGetAll , '/api/v1/cominggetall')
api.add_resource(ComingGetOne, '/api/v1/cominggetone/<id>')
api.add_resource(ComingHandler, '/api/v1/cominghandler')

#Sale
api.add_resource(SaleGetAll , '/api/v1/salegetall')
api.add_resource(SaleGetOne, '/api/v1/salegetone/<id>')
api.add_resource(SaleHandler, '/api/v1/salehandler')

#Balance
api.add_resource(BalanceGetAll , '/api/v1/balancegetall')
api.add_resource(BalanceGetOne, '/api/v1/balancegetone/<id>')
api.add_resource(BalanceHandler, '/api/v1/balancehandler')
