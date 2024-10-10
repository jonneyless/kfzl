from assist import get_current_time
from dbpool import OPMysql


# ======================================================================================================================

async def official_kefu_one(user_tg_id):
    opm = OPMysql()

    sql = "select id from offical_kefu where tg_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def group_link_save(group_tg_id, link, user_tg_id):
    opm = OPMysql()

    sql = "insert into group_link(group_tg_id, link, created_at, user_tg_id) values('%s', '%s', '%s', '%s')" % (
        group_tg_id, link, get_current_time(), user_tg_id)

    result = opm.op_update(sql)

    opm.dispose()

    return result


async def get_from(user_tg_id):
    opm = OPMysql()

    sql = "select * from froms where user_tg_id = '%s'" % user_tg_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def get_from_by_username(username):
    opm = OPMysql()

    sql = "select * from froms where username = '%s'" % username

    result = opm.op_select_one(sql)

    opm.dispose()

    return result


async def get_user(user_id):
    opm = OPMysql()

    sql = "select * from users where id = '%s'" % user_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result

async def get_sensitive_words():
    opm = OPMysql()

    sql = "select * from sensitive_words where 1 = 1"

    result = opm.op_select_all(sql)

    opm.dispose()

    words = []
    for word in result:
        words.append(word['name'])

    return words


async def getUserGroupIds(userId):
    opm = OPMysql()

    sql = "select group_tg_id from user_group_new where user_tg_id = '%s'" % userId

    result = opm.op_select_all(sql)

    opm.dispose()

    ids = []
    for data in result:
        ids.append(data['group_tg_id'])

    return ids


async def getGroupsByIds(groupIds, select="*"):
    opm = OPMysql()

    sql = opm.cur.mogrify("select %s from `groups` where chat_id in %s", (select, groupIds))

    result = opm.op_select_all(sql)

    return result
