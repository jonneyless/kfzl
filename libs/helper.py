import datetime
import json
import re
import time

import requests
from hydrogram.types import InlineKeyboardButton

import consts
from config import gqzlBotToken, welcomeApiUrl, danbao444ApiUrl, he444ApiUrl, createLinkUrl, callbackUrl
from libs.logger import logger


def getWelcomeApi(api):
    return "%s/%s" % (welcomeApiUrl, api)


def getDanbao444Api(api):
    return "%s/%s" % (danbao444ApiUrl, api)


def getHe444Api(api):
    return "%s/%s" % (he444ApiUrl, api)


def getDataFromApi(url, **kwargs):
    if 'params' in kwargs:
        params = kwargs['params']
    else:
        params = {}

    if 'key' not in params:
        params['key'] = 'huionedb'

    try:
        response = requests.get(url, params)
        data = response.json()
        logger.info('Request Url: ' + url)
        logger.info('Response Params: ' + json.dumps(params))
        logger.info('Response Data: ' + json.dumps(data))
        if "message" in data and data['message'] == 'success':
            return data['data']
    except Exception as e:
        logger.error('url: ' + url)
        logger.error('params: ' + json.dumps(params))
        logger.error(e)
        pass

    return None


def setDataByApi(url, **kwargs):
    if 'params' in kwargs:
        params = kwargs['params']
    else:
        params = {}

    if 'key' not in params:
        params['key'] = 'huionedb'

    try:
        response = requests.post(url, json=params)
        data = response.json()
        logger.info('Request Url: ' + url)
        logger.info('Response Params: ' + json.dumps(params))
        logger.info('Response Data: ' + json.dumps(data))
        if "message" in data and data['message'] == 'success':
            return data['data']
        logger.error('Request Failed. Params: %s, Response: %s' % (json.dumps(params), json.dumps(data)))
    except Exception as e:
        logger.error('Request Failed. Params: %s, Exception: %s' % (json.dumps(params), e))
        pass

    return None


def setDataForWelcome(api, **kwargs):
    return setDataByApi(getWelcomeApi(api), **kwargs)


def getDataFromHe444(api, **kwargs):
    return getDataFromApi(getHe444Api(api), **kwargs)


def getDataFromWelcome(api, **kwargs):
    return getDataFromApi(getWelcomeApi(api), **kwargs)


def setDataForDanbao444(api, **kwargs):
    return setDataByApi(getDanbao444Api(api), **kwargs)


def getDataFromDanbao444(api, **kwargs):
    return getDataFromApi(getDanbao444Api(api), **kwargs)


def getUnUsedGroupNum():
    data = getDataFromDanbao444('dbgroupnums')
    if data is not None:
        return data

    return []


def getUserSpecialGroup(userId):
    data = getDataFromDanbao444('identity', params={'user_tg_id': userId})
    if data is not None and 'groups' in data:
        return len(data['groups'])

    return 0


def getUserCommonGroup(userId):
    data = getDataFromHe444('identity', params={'user_tg_id': userId})
    if data is not None and 'groups' in data:
        return len(data['groups'])

    return 0


def getUserCheatInfo(userId):
    return getDataFromDanbao444('cheatinfo', params={'user_tg_id': userId})


def getUserCheat(userId):
    return getDataFromDanbao444('cheat', params={'tgid': userId})


def getUserBlack(userId):
    return getDataFromDanbao444('black', params={'tgid': userId})


def getUserInfo(userId, type="gongqun"):
    return getDataFromWelcome('kefu/userinfo', params={'user_tg_id': userId, 'type': type})


def userUnCheat(userId):
    data = setDataForDanbao444('cache/delCheatSpecial', params={'key': 'huionedb4', 'tgid': userId})
    if data is not None:
        return True

    return False


def userUnBlack(userId):
    data = setDataForDanbao444('cache/delCheat', params={'key': 'huionedb4', 'tgid': userId})
    if data is not None:
        return True

    return False


def userUnban(userId, actType, groupType):
    data = getDataFromWelcome('kefu/unban', params={'user_tg_id': userId, 'type': actType, 'grouptype': groupType})
    if data is not None:
        return True

    return False


def userGQUnBlack(userId, callbackData=None):
    if callbackData is None:
        data = getDataFromWelcome('kefu/cancelRestrictGongqun', params={'user_tg_id': userId, 'callback_data': {}, 'callback_url': 'http://huione.test'})
    else:
        data = getDataFromWelcome('kefu/cancelRestrictGongqun', params={'user_tg_id': userId, 'callback_data': callbackData, 'callback_url': callbackUrl})
    if data is not None:
        return True

    return False


def userGQUnban(userId, callbackData=None):
    if callbackData is None:
        data = getDataFromWelcome('kefu/unbanGongqun', params={'user_tg_id': userId, 'callback_data': {}, 'callback_url': 'http://huione.test'})
    else:
        data = getDataFromWelcome('kefu/unbanGongqun', params={'user_tg_id': userId, 'callback_data': callbackData, 'callback_url': callbackUrl})
    if data is not None:
        return True

    return False


def checkCheatList(username):
    data = getDataFromDanbao444('checkCheat', params={'username': username})
    if data is not None and "flag" in data:
        return data

    return None


def getPastAds():
    startTime = int(time.mktime(datetime.date.today().timetuple())) + 3600
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
            pattern = r'公群(\d*)'
            result = re.search(pattern, ad)
            if result is not None and result.group(0) == groupNumText:
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


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_current_timestamp():
    return int(time.time())


def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def createBotApproveLink(groupTgId):
    tg_url = 'https://api.telegram.org/bot' + gqzlBotToken + '/createChatInviteLink'
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": groupTgId,
    }

    current_timestamp = get_current_timestamp()

    data["name"] = "单个链接"
    data["creates_join_request"] = False
    data["expire_date"] = current_timestamp + 86400
    data["member_limit"] = 1

    response = requests.post(tg_url, json=data, headers=headers, timeout=30)

    link = None
    if response is not None:
        data = response.json()

        if ("result" in data) and data["result"]:
            link = data["result"]["invite_link"]

    return link


def getGroupBackupData():
    return getDataFromDanbao444("kefu/beiyong")


def getGroupInfo(title):
    return getDataFromDanbao444("kefu/groupinfo", params={'title': title})


def setGroupTitle(groupId, title, userTgId, username, fullname):
    return setDataForDanbao444("kefu/settitle", params={'group_tg_id': groupId, 'title_new': title, 'user_tg_id': userTgId, 'username': username, 'fullname': fullname})


def createAdLink(groupNum, monthAd, auditLink):
    headers = {
        "Content-Type": "application/json",
    }

    linkType = 4
    if monthAd and not auditLink:
        linkType = 5
    elif not monthAd and auditLink:
        linkType = 7
    elif monthAd and auditLink:
        linkType = 8

    data = {
        "key": "huionedb2",
        "num": groupNum,
        "type": linkType
    }

    response = requests.post(createLinkUrl, json=data, headers=headers, timeout=30)

    link = None
    title = '公群' + groupNum
    if response is not None:
        data = response.json()

        if ("message" in data) and data["message"] == "success":
            link = data["data"]["link"]
            if 'title' in data["data"]:
                title = data["data"]["title"]

    return link, title


def buildUnblockButton(text, userId, selected, selfValue, status):
    if selected is not None:
        if (selected & selfValue) == selfValue:
            text = "✅️" + text
            return InlineKeyboardButton(text=text, callback_data=consts.callback_data.CallBackUnblock + ':' + userId + ':' + str(selected ^ selfValue) + ':' + ','.join(status))
    else:
        selected = selfValue
    return InlineKeyboardButton(text=text, callback_data=consts.callback_data.CallBackUnblock + ':' + userId + ':' + str(selected | selfValue) + ':' + ','.join(status))


def formatDatetime(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def setBlack(userId, optId, reason):
    data = setDataForWelcome("kefu/addCheat", params={'key': 'huionedb4', 'tgid': userId, 'ope_user_tg_id': optId, 'reason': reason})
    if data is not None:
        return True

    return False


def setCheat(userId, optId, reason):
    data = setDataForWelcome("kefu/addCheatSpecial", params={'key': 'huionedb4', 'tgid': userId, 'ope_user_tg_id': optId, 'reason': reason})
    if data is not None:
        return True

    return False


def checkOfficial(userId):
    data = getDataFromWelcome('kefu/official', params={'tgid': userId})
    if data is not None and "flag" in data:
        return data['flag'] == 1

    return False
