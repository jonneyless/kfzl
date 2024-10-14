from datetime import datetime
from typing import List

from database.mysql import *
from database.redis import cache


def NewGroupLink(groupTgId, userTgId, link):
    model = GroupLink()
    model.group_tg_id = groupTgId
    model.user_tg_id = userTgId
    model.link = link
    model.created_at = datetime.now()
    model.save()

    return model


def checkIsKefu(tgId):
    return OfficialKefu.select().where(OfficialKefu.tg_id == str(tgId)).exists()


def getSensitiveWords() -> List[str]:
    key = "sensitive:words"
    words = cache.get(key)
    if words is None:
        words = []
        data = SensitiveWords.select()
        for datum in data:
            if datum.name not in words:
                words.append(datum.name)
        cache.set(key, words, 600)
    return words


def getFrom(userId) -> Froms | None:
    return Froms.get_or_none(Froms.user_tg_id == str(userId))


def getKefu(userId) -> Users | None:
    return Users.get_or_none(Users.id == userId)
