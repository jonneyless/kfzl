import re
from asyncio import futures

from telethon import TelegramClient

import db
import db_redis
import helpp


def isNumber(text: str) -> bool:
    if text is None:
        return False

    try:
        float(text)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(text)
        return True
    except (TypeError, ValueError):
        pass
    return False


async def index(bot: TelegramClient, event, chat_id, sender_id, text, message):
    if text == "/start":
        await event.reply("kefuZLbot")
        return

    official = await db.official_kefu_one(sender_id)
    if official is None:
        await event.reply("error...")
        return

    if isNumber(text):
        user = await db.get_from(text)
        if user is not None:
            kefu = await db.get_user(user['user_id'])
            if kefu is not None:
                await event.reply("飞机号：%s\n帐号：@%s\n所属客服：%s %s" % (user['user_tg_id'], user['username'], kefu['nickname'], kefu['name']))
            else:
                await event.reply("飞机号：%s\n帐号：@%s\n所属客服：%s %s" % (user['user_tg_id'], user['username'], "", ""))
        else:
            await event.reply("用户不存在")
        return

    if text == "广告":
        async with bot.conversation(event.sender_id, timeout=60) as conv:
            try:
                await conv.send_message('请输入广告内容')
                response = await conv.get_response()
                answer = response.text

                notifies = []
                if len(answer) > 157:
                    notifies.append('* 广告内容字数157字符超数')

                sensitiveWords = await db_redis.get_sensitive_words()
                words = []
                for word in sensitiveWords:
                    if answer.find(word) > -1:
                        words.append(word)

                if len(words) > 0:
                    notifies.append('* 广告内容出现违禁词“%s”' % ("”, “".join(words)))

                pattern = r'\@\S+'
                usernames = re.findall(pattern, answer)
                if len(usernames) > 0:
                    result = helpp.check_user(usernames)
                    if len(result) > 0:
                        for notify in result:
                            notifies.append(notify)

                if len(notifies) > 0:
                    notifies.append('请及时修改。')
                    return event.reply("\n".join(notifies))


            except futures.TimeoutError as e:
                return await event.respond('未检测到广告内容')
                pass


    if text == "未启用群编号":
        data = helpp.getUnUsedGroupNum()
        chunk = []
        for i in range(0, len(data), 400):
            chunk.append(data[i:i + 400])

        for items in chunk:
            await event.reply(", ".join(map(str, items)))

        await event.reply("数目： %s" % len(data))
        return

    await event.reply("创建链接已停用")

    # group_tg_id = False
    # if text == "SVIP群":
    #     group_tg_id = "-1001601629727"
    # elif text == "VIP群":
    #     group_tg_id = "-1001753191368"
    # elif text == "盘总群":
    #     group_tg_id = "-1001824105782"
    # elif text == "招聘群":
    #     group_tg_id = "-1001986586516"
    # elif text == "黑客群":
    #     group_tg_id = "-1001950107503"
    # elif text == "站长群":
    #     group_tg_id = "-1001910194051"
    # elif text == "美工/搭建群":
    #     group_tg_id = "-1001821490286"
    # elif text == "账号群":
    #     group_tg_id = "-1001927554058"
    # elif text == "test":
    #     group_tg_id = "-1001677560391"
    #
    # if not group_tg_id:
    #     await event.reply("信息错误")
    #     return
    #
    # link = await tg.createBotApproveLink(group_tg_id)
    # if link is None:
    #     await event.reply("创建链接失败，请重试")
    #     return
    #
    # await db.group_link_save(group_tg_id, link, sender_id)
    #
    # msg = text
    # msg += "\n单日单人链接\n"
    # msg += link
    # await event.reply(msg)