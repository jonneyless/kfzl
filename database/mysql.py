from peewee import Model, CharField, SmallIntegerField, BigIntegerField, IntegerField, DecimalField, DateTimeField
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

from config.config import db

db_config = {
    'host': db.HOST,
    'port': db.PORT,
    'user': db.USER,
    'password': db.PASS,
    'database': db.DATABASE,
}


class UnsignedBigIntegerField(BigIntegerField):
    field_type = 'BIGINT UNSIGNED'


class UnsignedIntegerField(IntegerField):
    field_type = 'INT UNSIGNED'


class UnsignedSmallIntegerField(SmallIntegerField):
    field_type = 'SMALLINT UNSIGNED'


class UnsignedTinyIntegerField(SmallIntegerField):
    field_type = 'TINYINT UNSIGNED'


class ReconnectPooledMySQLDatabase(ReconnectMixin, PooledMySQLDatabase):
    _instance = None

    @classmethod
    def get_db_instance(cls):
        if not cls._instance:
            cls._instance = cls(**db_config, max_connections=10)
        return cls._instance


class Mysql():
    def __init__(self):
        self.db = ReconnectPooledMySQLDatabase.get_db_instance()
        self.db.connect()

    def Conn(self):
        return self.db


mysql = Mysql()


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = mysql.Conn()


class Froms(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    user_id = UnsignedBigIntegerField()
    user_tg_id = CharField(max_length=64)
    fullname = CharField(max_length=255, default='')
    firstname = CharField(max_length=255, default='')
    lastname = CharField(max_length=255, default='')
    username = CharField(max_length=255, default='')
    remark = CharField(max_length=255, default='')
    avatar = CharField(max_length=255, default='')
    yajin_num = UnsignedIntegerField(default=0)
    yajin_money = DecimalField(max_digits=20, decimal_places=2, default=0.00)

    class Meta:
        table_name = "froms"


class Bots(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    tg_id = CharField(max_length=64)
    username = CharField(max_length=255)
    token = CharField(max_length=255)
    fullname = CharField(max_length=255)
    type = IntegerField(default=-1)
    sortt = IntegerField(default=-1)
    type_back = IntegerField()
    is_all = IntegerField(default=2)

    class Meta:
        table_name = "bots"


class BotGroup(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    group_tg_id = CharField(max_length=64)
    user_tg_id = CharField(max_length=64)
    type = UnsignedIntegerField(default=1)

    class Meta:
        table_name = "bot_group"


class Users(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    business_id = UnsignedIntegerField()
    name = CharField(max_length=255)
    nickname = CharField(max_length=255, default='')
    password = CharField(max_length=255)
    remember_token = CharField(max_length=255, default='')
    avatar = CharField(max_length=255, default='')

    class Meta:
        table_name = "users"


class GroupLink(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    group_tg_id = CharField(max_length=64)
    user_tg_id = CharField(max_length=64)
    link = CharField(max_length=255)
    type = IntegerField()
    status = IntegerField(default=1)
    created_at = DateTimeField()

    class Meta:
        table_name = "group_link"


class OfficialKefu(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    tg_id = CharField(max_length=64)
    fullname = CharField(max_length=255, default='')
    username = CharField(max_length=255, default='')

    class Meta:
        table_name = "offical_kefu"


class SensitiveWords(BaseModel):
    id = UnsignedBigIntegerField(index=True)
    name = CharField(max_length=64)

    class Meta:
        table_name = "sensitive_words"
