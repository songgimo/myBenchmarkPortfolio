from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api


from KiwoomHighChart.api import GetDailyCandle, GetStockIndicators, PutStockIndicators

app = Flask(__name__)
api = Api()

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api.add_resource(GetDailyCandle, '/api/v0/get/daily-candle')

api.add_resource(GetStockIndicators, '/api/v0/get/indicators')
api.add_resource(PutStockIndicators, '/api/v0/put/indicators')
api.init_app(app)


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, threaded=True)
