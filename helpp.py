import re
import time

import requests


def getUnUsedGroupNum():
    url = "http://welcome.444danbao.com/api/dbgroupnums?key=huionedb"

    try:
        response = requests.get(url)
        data = response.json()
        return data['data']
    except Exception as e:
        pass

    return []


def checkCheatList(username):
    url = "http://welcome.444danbao.com/api/checkCheat?key=huionedb&username=%s" % username

    response = requests.get(url, timeout=30)

    if response is not None:
        result = response.json()
        if "message" in result:
            if result["message"] == "success":
                if "flag" in result["data"]:
                    return result["data"]

    return None


def getPastAds():
    startTime = int(time.time()) - 3600 * 24
    url = "http://qunguan.huionedanbao.com:8680/api/gongqiu?key=huionedb&start=%s" % startTime

    response = requests.get(url, timeout=30)

    ads = []
    if response is not None:
        result = response.json()
        if "data" in result:
            for datum in result["data"]:
                ads.append(datum['text'])

    return ads


def check_user(usernames):
    notifies = []

    cheat = False
    repeat = False
    ads = getPastAds()

    allContacts = []
    for ad in ads:
        pattern = r'\@(\S+)'
        contacts = re.findall(pattern, ad)
        for contact in contacts:
            if contact not in allContacts:
                allContacts.append(contact)

    for username in usernames:
        if not cheat:
            cheatsSpecial = checkCheatList(username)
            if int(cheatsSpecial['flag']) == 1:
                cheat = True

        if not repeat:
            if len(allContacts) > 0:
                if username in allContacts:
                    repeat = True

    if cheat:
        notifies.append('* 注意⚠️该广告联系人在骗子库')

    if repeat:
        notifies.append('* 该广告存在发布重复风险，请再次确认广告内容')

    return notifies


def check_group_num(groupNum):
    text = "公群" + str(groupNum)
    ads = getPastAds()
    for ads in ads:
        if text in ads:
            return False

    return True
