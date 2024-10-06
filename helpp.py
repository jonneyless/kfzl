import requests
from zhon.pinyin import a_word

import db


def getUnUsedGroupNum():
    url = "http://welcome.444danbao.com/api/dbgroupnums?key=huionedb"

    try:
        response = requests.get(url)
        data = response.json()
        return data['data']
    except Exception as e:
        pass

    return []


def checkCheatList(userTgId):
    url = "http://welcome.444danbao.com/api/cheat?key=huionedb&tgid=%s" % userTgId

    response = requests.get(url, timeout=30)

    if response is not None:
        result = response.json()
        if "message" in result:
            if result["message"] == "success":
                if "flag" in result["data"]:
                    return result["data"]

    return None


async def check_user(usernames):
    notifies = []
    for username in usernames:
        user = await db.get_from_by_username(username)
        if user is not None:
            cheatsSpecial = checkCheatList(user['user_tg_id'])
            if int(cheatsSpecial['flag']) == 1:
                notifies.append('* 注意⚠️该广告联系人在骗子库')
                break

    return notifies
