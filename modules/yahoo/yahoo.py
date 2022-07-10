from modules.yahoo.settings import *

import requests


class YahooFinanceAPI(object):
    def __init__(self):
        super(YahooFinanceAPI, self).__init__()

    def __validate_parameter(self, parameter):
        symbols = parameter.get('symbols')
        if symbols:
            if not isinstance(str, symbols):
                if len(symbols) > 10:
                    # add log
                    return False, parameter, ''
                parameter['symbols'] = ','.join(symbols)

        return True, parameter, ''

    def _get_request(self, path, parameter=None):
        if parameter is None:
            parameter = dict()

        is_valid, parameter, message = self.__validate_parameter(parameter)

        if not is_valid:
            raise

        url = '/'.join([Urls.BASE, path])

        response = requests.get(url, parameter)

        if not response.ok:
            raise

        return response.json()

    def get_bulk_close_history(self, interval, range_, symbols):
        parameters = {
            "interval": interval,
            "range": range_,
            "symbols": symbols
        }
        return self._get_request(Urls.SPARK, parameters)
