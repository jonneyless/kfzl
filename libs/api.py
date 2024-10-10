import requests

from config import tgApiUrl


def sendMessage(params):
    tg_url = tgApiUrl + "sendMessage"

    try:
        req = requests.post(tg_url, json=params, headers={
            "Content-Type": "application/json",
        }, timeout=15)

        data = req.json()
        if 'ok' in data and not data['ok']:
            raise Exception("%s %s" % (params['chat_id'], data['description']))

        return True
    except Exception as e:
        print("sendMessageOne Exception: %s" % e)
        return False


def createChatInviteLink(params):
    tg_url = tgApiUrl + "createChatInviteLink"

    try:
        req = requests.post(tg_url, json=params, headers={
            "Content-Type": "application/json",
        }, timeout=15)

        data = req.json()
        if 'ok' in data and not data['ok']:
            raise Exception("%s %s" % (params['chat_id'], data['description']))

        return data['result']["invite_link"]
    except Exception as e:
        print("createChatInviteLink Exception: %s" % e)
        return None
