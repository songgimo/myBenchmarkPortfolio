import redis

REDIS_SERVER = redis.StrictRedis(host='localhost', port=6379, db=0)


class RedisKeys(object):
    TX_DATA = 'tx-data'
