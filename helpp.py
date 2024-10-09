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


def check_ads(usernames, groupNum):
    groupNumText = "公群" + str(groupNum)
    notifies = []

    cheatUsername = []
    checkedUsername = []
    repeat = False
    groupNumRepeat = False
    ads = getPastAds()

    allContacts = []
    for ad in ads:
        if not groupNumRepeat:
            if groupNumText in ad:
                groupNumRepeat = True

        pattern = r'\@(\S+)'
        contacts = re.findall(pattern, ad)
        for contact in contacts:
            if contact not in allContacts:
                allContacts.append(contact)

    for username in usernames:
        if username not in checkedUsername:
            checkedUsername.append(username)

            cheatsSpecial = checkCheatList(username)
            if int(cheatsSpecial['flag']) == 1:
                cheatUsername.append(username)

        if not repeat:
            if len(allContacts) > 0:
                if username in allContacts:
                    repeat = True

    if len(cheatUsername) > 0:
        notifies.append('* 注意⚠️该广告联系人在骗子库 @%s' % ' @'.join(cheatUsername))

    if repeat:
        notifies.append('* 该广告存在发布重复风险，请再次确认广告内容')

    if groupNumRepeat:
        notifies.append('* 该广告发布重复')

    return notifies
