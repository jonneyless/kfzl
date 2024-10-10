import json

import peewee
import redis
from playhouse.shortcuts import model_to_dict, dict_to_model

from config.config import redis as config
from database.mysql import SensitiveWords


class Cache:
    def __init__(self):
        self.redis = redis.Redis(
            host=config.HOST,
            port=config.PORT,
            db=config.DB,
            encoding='utf8',
            decode_responses=True
        )
        self.prefix = config.PREFIX

    def getKey(self, key):
        return self.prefix + key

    def modelToDict(self, model):
        model = model_to_dict(model=model)
        if "created_at" in model:
            model.pop("created_at")
        if "updated_at" in model:
            model.pop("updated_at")
        return model

    def get(self, key, obj: SensitiveWords | None = None):
        value = self.redis.get(self.getKey(key))
        if value is None or value == "null":
            return None
        value = json.loads(str(value))
        if obj is not None:
            if isinstance(value, dict):
                value = dict_to_model(model_class=obj, data=value)
            elif isinstance(value, list):
                items = []
                for item in value:
                    item = dict_to_model(model_class=obj, data=item)
                    items.append(item)
                value = items
        return value

    def set(self, name, value, px):
        if isinstance(value, SensitiveWords):
            value = self.modelToDict(value)
        elif isinstance(value, peewee.ModelSelect):
            items = []
            for v in value:
                if isinstance(v, SensitiveWords):
                    v = self.modelToDict(v)
                items.append(v)
            value = items

        return self.redis.set(name=self.getKey(name), value=json.dumps(value), px=60 * 1000 * px)

    def delete(self, name):
        return self.redis.delete(self.getKey(name))

    def lock(self, name):
        return self.redis.lock(name, timeout=30)

    def hgetall(self, name):
        return self.redis.hgetall(self.getKey(name))

    def hset(self, name, key, value):
        return self.redis.hset(self.getKey(name), key, value)

    def hdel(self, name, key):
        return self.redis.hdel(self.getKey(name), key)

    def lpop(self, name):
        return self.redis.lpop(self.getKey(name))

    def rpush(self, name, values):
        return self.redis.rpush(self.getKey(name), values)


cache = Cache()
