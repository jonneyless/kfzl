import requests

from config import botToken, notifyBotToken, notifyGroupId
from libs.logger import logger


def sendMessage(params):
    return telegramApi('sendMessage', params)


def editMessage(params):
    return telegramApi('editMessageText', params)


def sendNotification(content):
    params = {
        "chat_id": notifyGroupId,
        "text": content,
    }

    return telegramApi('sendMessage', params, notifyBotToken)


def telegramApi(api, params, token=None):
    if token is None:
        token = botToken

    tg_url = "https://api.telegram.org/bot%s/%s" % (token, api)

    try:
        req = requests.post(tg_url, json=params, headers={
            "Content-Type": "application/json",
        }, timeout=15)

        data = req.json()
        if 'ok' in data and not data['ok']:
            raise Exception("%s %s" % (params['chat_id'], data['description']))

        return True
    except Exception as e:
        logger.error("%s Exception: %s" % (api, e))
        return False
