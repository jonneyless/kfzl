from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import consts
from database.mysql import Froms
from database.service import getFrom, getKefu
from handler.base import BaseHandler
from libs.helper import getUserCheat, getUserBlack, userUnCheat, userUnBlack


class CallbackHandler(BaseHandler):

    async def Customer(self):
        msg = await self.askUser()
        if msg is not None:
            user = await self.getUser(msg)
            if user is not None:
                kefuNickname = ''
                kefuName = ''
                kefu = getKefu(user.user_id)
                if kefu is not None:
                    kefuNickname = kefu.nickname
                    kefuName = kefu.name

                return await self.Reply("飞机号：%s\n帐号：@%s\n所属客服：%s %s" % (user.user_tg_id, user.username, kefuNickname, kefuName), msgId=msg.id)

    async def Unblock(self):
        msg = await self.askUser()
        if msg is not None:
            user = await self.getUser(msg)
            if user is not None:
                content = "客户的状态如下：\n"
                content += "飞机号：%s\n" % user.user_tg_id
                content += "帐号：@%s\n" % user.username

                buttons = []
                rows = []

                cheat = getUserCheat(user.user_tg_id)
                if cheat is not None and cheat['flag'] == 1:
                    content += "骗子库：是\n"
                    buttons.append(InlineKeyboardButton(text="移出骗子库", callback_data=consts.callback_data.CallBackUnCheat + ':' + user.user_tg_id))
                else:
                    content += "骗子库：否\n"

                black = getUserBlack(user.user_tg_id)
                if black is not None and black['flag'] == 1:
                    content += "黑名单：是，%s\n" % black['reason']
                    buttons.append(InlineKeyboardButton(text="移出黑名单", callback_data=consts.callback_data.CallBackUnBlack + ':' + user.user_tg_id))
                else:
                    content += "黑名单：否\n"

                if len(buttons) == 0:
                    return await self.Reply(content, msgId=msg.id)

                rows.append(buttons)

                return await self.Reply(content, msgId=msg.id, replyMarkup=InlineKeyboardMarkup(inline_keyboard=rows))

    async def UnCheat(self):
        userId = self.data.split(":")[1]
        if not userUnCheat(userId):
            await self.Respond('处理失败')
        else:
            user = getFrom(userId)
            await self.Respond('已将 @%s 移出骗子库' % user.username)

    async def UnBlack(self):
        userId = self.data.split(":")[1]
        if not userUnBlack(userId):
            await self.Respond('处理失败')
        else:
            user = getFrom(userId)
            await self.Respond('已将 @%s 移出黑名单' % user.username)

    async def askUser(self):
        msg = await self.Ask('请输入客户的tgId')

        if msg is None:
            await self.Alert('未收到客户的tgId')
        elif not self.isNumber(msg.text):
            await self.Alert('输入的tgId不正确')
        else:
            return msg

        return None

    async def getUser(self, msg) -> Froms | None:
        user = getFrom(msg.text)
        if user is None:
            await self.Reply('用户不存在', msgId=msg.id)
        else:
            return user

        return None
