import redis

REDIS_SERVER = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=15)


class RedisKeys(object):
    KIWOOM_API_KEY = 'kiwoom-api-key'
    KIWOOM_RESULT_KEY = 'kiwoom-result-key'
    TX_DATA = 'tx-data'
