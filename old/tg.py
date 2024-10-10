import json

import requests

from assist import get_current_timestamp
from config import bot_url


async def createBotApproveLink(group_tg_id):
    # 123群单个链接（一天1个人链接）

    tg_url = bot_url + "createChatInviteLink"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
    }

    current_timestamp = get_current_timestamp()
    forever_date = current_timestamp + 86400 * 3650

    data["name"] = "单个链接"
    data["creates_join_request"] = False
    data["expire_date"] = current_timestamp + 86400
    data["member_limit"] = 1

    response = requests.post(tg_url, json=data, headers=headers, timeout=30)

    link = None
    if response is not None:
        response_text = json.loads(response.text)

        if ("result" in response_text) and response_text["result"]:
            link = response_text["result"]["invite_link"]

    return link
