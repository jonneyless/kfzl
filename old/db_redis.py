import json

from redis import Redis

import db
from config import env

conn = Redis(host=env.str("REDIS_HOST", "127.0.0.1"), port=env.int("REDIS_PORT", 6379), db=env.int("REDIS_DB", 0))
prefix = env.str("REDIS_PREFIX", "chat_private")


async def get_sensitive_words():
    key = prefix + ":sensitive_words"

    cache = conn.get(key)
    if cache is not None:
        words = json.loads(cache)
    else:
        words = await db.get_sensitive_words()
        conn.set(key, json.dumps(words), 600)

    return words
