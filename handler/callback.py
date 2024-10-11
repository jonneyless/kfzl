from database.mysql import Froms
from database.service import getFrom, getKefu
from handler.base import BaseHandler
from libs.helper import getUserCheat, getUserBlack


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
                cheat = getUserCheat(user.user_tg_id)
                black = getUserBlack(user.user_tg_id)

                content = "客户的状态如下：\n"
                content += "飞机号：%s\n" % user.user_tg_id
                content += "帐号：@%s\n" % user.username

                buttons = []
                if cheat is not None and cheat['flag'] == 1:
                    content += "骗子库：是\n"
                    buttons.append(InlineKeyboardButton(text="客户板块", callback_data=consts.callback_data.CallBackCustomer))
                if black is not None and black['flag'] == 1:
                    content += "黑名单：是，%s\n" % black['reason']

                return await self.Reply(content, msgId=msg.id)

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
