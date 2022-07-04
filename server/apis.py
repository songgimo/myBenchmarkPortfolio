from flask_restful import Resource
from flask import jsonify, request

from server.queries import GetQueries


class GetDailyCandle(Resource):
    def get(self):
        args = request.args
        stock_code = args.get('stock_code')

        candles = GetQueries.all_candle_by_name(stock_code)

        if candles:
            return {
                "success": False,
                "data": {
                    "candles": candles
                },
                "message": ''
            }
        else:
            return {
                "success": False,
                "data": '',
                "message": ''
            }
