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
appId = env.int("APP_ID")
appHash = env.str("APP_HASH")
gqzlBotToken = env.str("GQZL_BOT_TOKEN")
notifyBotToken = env.str("NOTIFY_BOT_TOKEN")
notifyGroupId = env.int("NOTIFY_GROUP_ID")
logFile = env.str("LOG_FILE", 'logs/service.log')
logFormat = env.str("LOG_FORMAT", "%(asctime)s Line%(lineno)d [%(levelname)s] %(message)s")
logDateFormat = env.str("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S")
createLinkUrl = env.str("CREATE_LINK_URL")
welcomeApiUrl = env.str("WELCOME_API_URL")
danbao444ApiUrl = env.str("DANBAO444_API_URL")
he444ApiUrl = env.str("HE444_API_URL")
callbackUrl = env.str("CALLBACK_URL")
match env.str("LOG_LEVEL"):
    case "debug":
        logLevel = logging.DEBUG
    case "info":
        logLevel = logging.INFO
    case "error":
        logLevel = logging.ERROR
    case _:
        logLevel = logging.NOTSET
