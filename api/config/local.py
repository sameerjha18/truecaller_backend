from .base import BaseConfig


class LocalConfig(BaseConfig):
    DEBUG = True
    HOST = 'mongodb://127.0.0.1:27017/trueCallerBackend'
    SECRET_KEY = 'e9af51f2ab76cae4145e2522250de0e20ddb1683d2112d9af2f9e82194469435'
    SESSION_TYPE = 'filesystem'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
