from telethon import TelegramClient, events

import handle_private_message
from config import *

bot = TelegramClient('kfzl', app_id, app_hash).start(bot_token=bot_token)


def is_private(chat_id, sender_id):
    flag = False
    if chat_id == sender_id and sender_id > 0:
        flag = True

    return flag


@bot.on(events.NewMessage(incoming=True))
async def new_message(event):
    chat_id = event.chat_id
    sender_id = event.sender_id

    if sender_id is None:
        return

    chat_id = int(chat_id)
    sender_id = int(sender_id)

    message = event.message
    text = message.message

    if is_private(chat_id, sender_id):
        await handle_private_message.index(bot, event, chat_id, sender_id, text, message)
        # try:
        #     await handle_private_message.index(bot, event, chat_id, sender_id, text, message)
        # except:
        #     print("handle_private_message error...")


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    print("init...")

    main()
