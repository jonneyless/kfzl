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


async def get_user(user_id):
    opm = OPMysql()

    sql = "select * from users where id = '%s'" % user_id

    result = opm.op_select_one(sql)

    opm.dispose()

    return result
