import json

import requests

bot_url = "https://api.telegram.org/bot2094467068:AAEPpPFe2mxoT8eeWeg-rMBy-ArsQ3ER87Y/"


def revokeChatInviteLink(group_tg_id, link):
    tg_url = bot_url + "revokeChatInviteLink"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "chat_id": group_tg_id,
        "invite_link": link,
    }

    # current_timestamp = get_current_timestamp()

    response = requests.post(tg_url, json=data, headers=headers, timeout=10)

    flag = False
    if response is not None:
        response_text = json.loads(response.text)

        print(response_text)

        if ("result" in response_text) and response_text["result"]:
            flag = True

    return flag


revokeChatInviteLink("-1001679517247", "https://t.me/+bCrOHv9fLHIwNmFi")
