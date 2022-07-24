import yfinance
import datetime
import json
from flask import request
from flask_restful import Resource

# 내 주식을 입력 -> 차트에 노출됨 ->
# 벤치마크 주식을 입력 -> 차트에 노출됨
# 괴리감 계산


class Result(object):
    def __init__(self, success, data, message):
        self.__success = success
        self.__data = data
        self.__message = message

    def to_dict(self):
        return {
            "success": self.__success,
            "data": self.__data,
            "message": self.__message
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class GetChart(Resource):
    def get(self):
        args = request.args
        print(list(args))
        code_name = args.get("code")
        print(code_name)
        last_three_years = datetime.datetime.now() - datetime.timedelta(days=365*3)
        yf = yfinance.download(code_name, last_three_years.strftime("%Y-%m-%d"))

        axes_for_timestamp = [axes.timestamp() * 1000 for axes in yf.axes[0]]
        zip_for_close = list(zip(axes_for_timestamp, list(yf.Close)))

        return Result(True, zip_for_close, None).to_dict()

#
# class GetDailyCandle(Resource):
#     def get(self):
#         args = request.args
#         stock_code = args.get('stock_code')
#
#         candles = GetQueries.all_candle_by_name(stock_code)
#
#         if candles:
#             return {
#                 "success": False,
#                 "data": {
#                     "candles": candles
#                 },
#                 "message": ''
#             }
#         else:
#             return {
#                 "success": False,
#                 "data": '',
#                 "message": ''
#             }
