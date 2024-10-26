import time
from datetime import datetime
from typing import List

from peewee import SQL

from database.mysql import *
from database.redis import cache


def NewGroupLink(groupTgId, userTgId, link, linkType):
    model = GroupLink()
    model.group_tg_id = groupTgId
    model.user_tg_id = userTgId
    model.link = link
    model.type = linkType
    model.created_at = datetime.now()
    model.save()

    return model


def NewUnblockRecord(actionId, actionName, userId, types):
    model = FromUnblockRecords()
    model.action_tg_id = actionId
    model.action_name = actionName
    model.from_tg_id = userId
    model.type = types
    model.created_at = int(time.time())
    model.save()


def getUnCheatCount(userId) -> int:
    return FromUnblockRecords.select().where(SQL('from_tg_id = %s and `type` & 1 = 1' % userId)).count()


def getUnBlackCount(userId) -> int:
    return FromUnblockRecords.select().where(SQL('from_tg_id = %s and `type` & 2 = 2' % userId)).count()


def getUnblockRecords(userId) -> List[FromUnblockRecords]:
    return FromUnblockRecords.select().where(FromUnblockRecords.from_tg_id == userId).order_by(FromUnblockRecords.created_at.asc())


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
