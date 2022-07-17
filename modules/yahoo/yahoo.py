from modules.yahoo.settings import *

import requests
import decimal
import time


class YahooFinanceAPI(object):
    def __init__(self):
        super(YahooFinanceAPI, self).__init__()
        self.__cache_refresh_time = 30
        self.__cached = {each: {"timestamp": None, "data": int(time.time())} for each in Consts.API_LIST}

    def __symbol_checker(self, parameter):
        symbols = parameter.get('symbols')
        if symbols:
            if not isinstance(str, symbols):
                if len(symbols) > 10:
                    # add log
                    return False, parameter, 'symbol 최대 입력 값은 10개입니다.'
                parameter['symbols'] = ','.join(symbols)
            return True, parameter, ''
        else:
            return False, parameter, 'symbol값은 필수입니다.'

    def __get_request(self, path, parameter=None):
        url = '/'.join([Urls.BASE, path])

        response = requests.get(url, parameter)

        if not response.ok:
            raise

        return response.json()

    def _get_spark(self, parameter):
        is_valid, parameter, message = self.__symbol_checker(parameter)

        if not is_valid:
            print(message)
            raise

        result = self.__get_request(Urls.SPARK, parameter)
        return result

    def _get_quote_summary(self, parameter):
        is_valid, parameter, message = self.__symbol_checker(parameter)

        if not is_valid:
            print(message)
            raise

        modules_ = parameter.get('modules')

        if not modules_:
            raise

        if modules_.title() not in QuoteSummary.keys():
            raise

        return self.__get_request(Urls.QUOTE, parameter)

    def get_bulk_close_history(self, interval, range_, symbols):
        parameter = {
            "interval": interval,
            "range": range_,
            "symbols": symbols
        }

        result = self._get_spark(parameter)

        close_by_symbol = dict()
        for symbol in result.keys():
            timestamp = result[symbol]["timestamp"]
            close = result[symbol]["close"]

            close_by_symbol[symbol] = list(zip(timestamp, close))

        return close_by_symbol

    def get_dividend_data(self, region, language, symbols):
        parameter = {
            "region": region,
            "lang": language,
            "symbols": symbols
        }
        result = self._get_quote_summary(parameter)

        data_by_symbol = dict()
        for each in result["quoteResponse"]["result"]:
            symbol = each["symbol"]
            data_by_symbol[symbol] = decimal.Decimal(each["trailingAnnualDividendRate"])
            data_by_symbol[symbol] = decimal.Decimal(each["trailingAnnualDividendYield"])

        return data_by_symbol