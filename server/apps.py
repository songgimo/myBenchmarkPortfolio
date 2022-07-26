from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from server.apis import GetChart

app = Flask(__name__)
api = Api()

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

api.add_resource(GetChart, '/api/v0/get/last-three-years-chart')
api.init_app(app)


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, threaded=True)
