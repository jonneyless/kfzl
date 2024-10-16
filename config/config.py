import logging

from environs import Env

env = Env()
env.read_env()


class DB:
    HOST = None
    PORT = None
    DATABASE = None
    USER = None
    PASS = None

    def __init__(self):
        self.HOST = env.str("DB_HOST")
        self.PORT = env.int("DB_PORT")
        self.DATABASE = env.str("DB_DATABASE")
        self.USER = env.str("DB_USER")
        self.PASS = env.str("DB_PASS")


db = DB()


class Redis:
    HOST = None
    PORT = None
    DB = None
    PREFIX = None

    def __init__(self):
        self.HOST = env.str("REDIS_HOST")
        self.PORT = env.int("REDIS_PORT")
        self.DB = env.str("REDIS_DB")
        self.PREFIX = env.str("REDIS_PREFIX")


redis = Redis()

md5salt = "x&df9P*a"
botToken = env.str("BOT_TOKEN")
botId = env.int("BOT_ID")
gqzlBotToken = env.str("GQZL_BOT_TOKEN")
appId = env.int("APP_ID")
notifyGroupId = env.int("NOTIFY_GROUP_ID")
appHash = env.str("APP_HASH")
logFile = env.str("LOG_FILE", 'logs/service.log')
logFormat = env.str("LOG_FORMAT", "%(asctime)s Line%(lineno)d [%(levelname)s] %(message)s")
logDateFormat = env.str("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
tgApiUrl = env.str("TG_API_URL")
match env.str("LOG_LEVEL"):
    case "debug":
        logLevel = logging.DEBUG
    case "info":
        logLevel = logging.INFO
    case _:
        logLevel = logging.NOTSET
