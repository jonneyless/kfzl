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


def getUserSpecialGroup(userId):
    url = "http://welcome.444danbao.com/api/identity?key=huionedb&user_tg_id=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return len(data['data']['groups'])
    except Exception as e:
        pass

    return 0


def getUserCommonGroup(userId):
    url = "http://he444.444danbao.com/api/identity?key=huionedb&user_tg_id=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return len(data['data']['groups'])
    except Exception as e:
        pass

    return 0


def getUserCheatInfo(userId):
    url = "http://welcome.444danbao.com/api/cheatinfo?key=huionedb&user_tg_id=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return data['data']
    except Exception as e:
        pass

    return []


def getUserCheat(userId):
    url = "http://welcome.444danbao.com/api/cheat?key=huionedb&tgid=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return data['data']
    except Exception as e:
        pass

    return None


def userUnCheat(userId):
    url = "http://welcome.444danbao.com/api/unban?key=huionedb&tgid=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return True
    except Exception as e:
        pass

    return False


def getUserBlack(userId):
    url = "http://welcome.444danbao.com/api/black?key=huionedb&tgid=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return data['data']
    except Exception as e:
        pass

    return None


def userUnBlack(userId):
    url = "http://welcome.444danbao.com/api/unban?key=huionedb&tgid=%s" % userId

    try:
        response = requests.get(url)
        data = response.json()
        if "message" in data and data['message'] == 'success':
            return True
    except Exception as e:
        pass

    return False


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


def getWebInfo(username):
    tg_url = "https://t.me/%s" % username

    headers = {
        "Content-Type": "application/json",
    }

    response = None

    try:
        response = requests.get(tg_url, headers=headers, timeout=30)
    except:
        pass

    if response is not None:
        return response.text

    return None


def checkIsUser(content):
    if content is not None:
        pattern = r'href="/s/'
        result = re.findall(pattern, content)
        if len(result) > 0:
            return 1

        pattern = r'>[0-9 ]*subscribers<'
        result = re.findall(pattern, content)
        if len(result) > 0:
            return 1

        pattern = r'>[0-9 ]*members<'
        result = re.findall(pattern, content)
        if len(result) > 0:
            return 1

        pattern = r'>View in Telegram<'
        result = re.findall(pattern, content)
        if len(result) > 0:
            return 1

        pattern = r'tgme_page_description[^"]*">\s*(.*)\s*<\/div>'
        result = re.findall(pattern, content)
        if len(result) > 0:
            if 'you can contact' in result[0]:
                return 2

    return 0


def getBio(content):
    if content is not None:
        pattern = r'tgme_page_description[^"]*">\s*(.*)\s*<\/div>'
        result = re.findall(pattern, content)
        if len(result) > 0:
            return result[0]

    return None


def checkAds(usernames, groupNum):
    groupNumText = "公群" + str(groupNum)
    notifies = []

    cheatUsername = []
    notUser = []
    notExists = []
    bioInfos = []
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
        webInfo = getWebInfo(username)
        isUser = checkIsUser(webInfo)
        if isUser == 1:
            notUser.append(username)
            continue
        elif isUser == 2:
            notExists.append(username)
            continue

        cheatsSpecial = checkCheatList(username)
        if cheatsSpecial is not None and int(cheatsSpecial['flag']) == 1:
            cheatUsername.append(username)

        if not repeat:
            if len(allContacts) > 0:
                if username in allContacts:
                    repeat = True

        bio = getBio(webInfo)
        if bio is not None:
            if re.search(r'@\S+', bio) is not None or re.search(r'https?://', bio) is not None:
                bioInfos.append("<b>" + username + "</b>：" + bio)

    if len(notUser) > 0:
        notifies.append('* 联系人 @%s 非普通用户' % ' @'.join(notUser))

    if len(notExists) > 0:
        notifies.append('* 联系人 @%s 不存在' % ' @'.join(notUser))

    if len(cheatUsername) > 0:
        notifies.append('* 注意⚠️该广告联系人在骗子库 @%s' % ' @'.join(cheatUsername))

    if repeat:
        notifies.append('* 该广告存在发布重复风险，请再次确认广告内容')

    if groupNumRepeat:
        notifies.append('* 该广告发布重复')

    if len(bioInfos) > 0:
        notifies.append("\n<b>可疑联系人简介</b>\n\n" + '\n\n'.join(bioInfos))

    return notifies
