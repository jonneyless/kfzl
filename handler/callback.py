from database.service import getFrom, getKefu
from handler.base import BaseHandler


class CallbackHandler(BaseHandler):

    async def Customer(self):
        msg = await self.Ask('请输入客户的tgId')

        if msg is None:
            await self.Alert('未收到客户的tgId')
        elif not self.isNumber(msg.text):
            await self.Alert('输入的tgId不正确')
        else:
            user = getFrom(msg.text)
            if user is None:
                return await self.Reply('用户不存在', msgId=msg.id)

            kefu = getKefu(user.user_id)
            if kefu is None:
                return await self.Reply("飞机号：%s\n帐号：@%s\n所属客服：%s %s" % (user.user_tg_id, user.username, "", ""), msgId=msg.id)
            else:
                return await self.Reply("飞机号：%s\n帐号：@%s\n所属客服：%s %s" % (user.user_tg_id, user.username, kefu.nickname, kefu.name), msgId=msg.id)
