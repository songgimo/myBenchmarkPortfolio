from modules.global_settings import REDIS_SERVER
from decimal import Decimal, getcontext, InvalidOperation
import json

getcontext().prec = 8


def get_redis(key, use_decimal=False):
    try:
        value = REDIS_SERVER.get(key)

        if not value:
            return None

        if use_decimal:
            json_to_dict_value = json.loads(value, cls=DecimalDecoder)
        else:
            json_to_dict_value = json.loads(value)

        return json_to_dict_value
    except:
        return None


def set_redis(key, value, use_decimal=False):
    """
        key: str
        value: dict
    """
    if use_decimal:
        dict_to_json_value = json.dumps(value, cls=DecimalEncoder)
    else:
        dict_to_json_value = json.dumps(value)
    REDIS_SERVER.set(key, dict_to_json_value)

    return


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class DecimalDecoder(json.JSONDecoder):
    def decode_converter(self, type_, tc, dic=False):
        for k in tc:
            if isinstance(k, list):
                type_.append(list())
                self.decode_converter(type_[-1], k)
            elif isinstance(k, dict):
                type_.append(dict())
                self.decode_converter(type_[-1], k, True)
            else:
                if dic:
                    if isinstance(tc[k], list):
                        type_[k] = list()
                        self.decode_converter(type_[k], tc[k])
                    elif isinstance(tc[k], dict):
                        type_[k] = dict()
                        self.decode_converter(type_[k], tc[k], True)
                    else:
                        if isinstance(tc[k], (float, int, str)):
                            try:
                                type_[k] = Decimal(tc[k])
                            except InvalidOperation:
                                type_[k] = tc[k]
                        else:
                            type_[k] = tc[k]
                else:
                    if isinstance(k, (float, int, str)):
                        try:
                            type_.append(Decimal(k))
                        except InvalidOperation:
                            type_.append(k)
                    else:
                        type_.append(k)
