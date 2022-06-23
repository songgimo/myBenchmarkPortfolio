import redis

REDIS_SERVER = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=15)


class RedisKeys(object):
    KIWOOM_API_KEY = 'kiwoom-api-key'
    COM_TO_MODULE_RESULT_KEY = 'com-to-module-result-key'
    COM_TO_SERVICE_RESULT_KEY = 'com-to-service-result-key'
    COM_COMMAND_KEY = 'com-command-key'
    TX_DATA = 'tx-data'
