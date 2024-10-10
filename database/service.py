from typing import List

from database.mysql import *
from database.redis import cache


def checkIsKefu(tgId):
    return OfficialKefu.select().where(OfficialKefu.tg_id == str(tgId)).exists()


def getSensitiveWords() -> List[str]:
    key = "sensitive:words"
    words = cache.get(key)
    if words is None:
        words = []
        data = SensitiveWords.select()
        for datum in data:
            words.append(datum.name)
        cache.set(key, words, 600)
    return words


def getFrom(userId) -> Froms | None:
    return Froms.get_or_none(Froms.user_tg_id == str(userId))
