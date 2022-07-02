import redis

REDIS_SERVER = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=15)


class RedisKeys(object):
    class Kiwoom(object):
        base = 'kiwoom'

        API_KEY = f'{base}-api-key'
        COM_TO_MODULE_RESULT_KEY = f'{base}-com-to-module-result-key'
        COM_TO_SERVICE_RESULT_KEY = f'{base}-com-to-service-result-key'
        COM_COMMAND_KEY = f'{base}-com-command-key'
        TX_DATA = f'{base}-tx-data'
