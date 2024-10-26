import re

from hydrogram.types import InlineKeyboardButton

import consts
from database.service import getFrom, getKefu, getSensitiveWords
from handler.base import BaseHandler
from handler.group import GroupHandler
from libs.helper import getUserCheat, getUserBlack, userUnCheat, userUnBlack, checkAds, createAdLink


class CallbackHandler(BaseHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = GroupHandler(client=self.client, data=self.oData, logger=self.logger)

    async def Customer(self):
        msg = await self.askUser()
        if msg is not None:
            user = getFrom(msg.text)
            if user is None:
                return await self.Reply('用户不存在', msgId=msg.id)

            kefuNickname = ''
            kefuName = ''
            kefu = getKefu(user.user_id)
            if kefu is not None:
                kefuNickname = kefu.nickname
                kefuName = kefu.name

            return await self.Reply("飞机号：<code>%s</code>\n帐号：@<code>%s</code>\n所属客服：%s %s" % (user.user_tg_id, user.username, kefuNickname, kefuName), msgId=msg.id)

    async def Unblock(self):
        msg = await self.askUser()
        if msg is not None:
            content = "客户的状态如下：\n"
            content += "飞机号：<code>%s</code>\n" % msg.text

            user = getFrom(msg.text)
            if user is not None:
                content += "帐号：@<code>%s</code>\n" % user.username

            buttons = []
            rows = []

            cheat = getUserCheat(msg.text)
            if cheat is not None and cheat['flag'] == 1:
                content += "骗子库：是，%s, %s\n" % (cheat['reason'], cheat['ope_user'])
                buttons.append(InlineKeyboardButton(text="移出骗子库", callback_data=consts.callback_data.CallBackUnCheat + ':' + msg.text))
            else:
                content += "骗子库：否\n"

            black = getUserBlack(msg.text)
            if black is not None and black['flag'] == 1:
                content += "黑名单：是，%s, %s\n" % (black['reason'], black['ope_user'])
                buttons.append(InlineKeyboardButton(text="移出黑名单", callback_data=consts.callback_data.CallBackUnBlack + ':' + msg.text))
            else:
                content += "黑名单：否\n"

            if len(buttons) == 0:
                return await self.Reply(content, msgId=msg.id)

            rows.append(buttons)

            return await self.Reply(content, msgId=msg.id, replyMarkup=rows)

    async def UnCheat(self):
        userId = self.data.split(":")[1]
        if not userUnCheat(userId):
            await self.Respond('处理失败')
        else:
            user = getFrom(userId)
            if user is not None:
                await self.Respond('已将 @%s 移出骗子库' % user.username)
            else:
                await self.Respond('已将 %s 移出骗子库' % userId)

    async def UnBlack(self):
        userId = self.data.split(":")[1]
        if not userUnBlack(userId):
            await self.Respond('处理失败')
        else:
            user = getFrom(userId)
            if user is not None:
                await self.Respond('已将 @%s 移出黑名单' % user.username)
            else:
                await self.Respond('已将 %s 移出黑名单' % userId)

    async def askUser(self):
        msg = await self.Ask('请输入客户的tgId')

        if msg is None:
            await self.Alert('未收到客户的tgId')
        elif not self.isNumber(msg.text):
            await self.Alert('输入的tgId不正确')
        else:
            return msg

        return None

    async def adLink(self):
        msg = await self.Ask('请输入获取指令')
        if msg is None:
            return await self.Respond('未检测到指令')

        pattern = r'(.*?)群(月?)广告(审核|)链接'
        result = re.match(pattern, msg.text)
        if result is None:
            return await self.Reply('指令错误', msgId=msg.id)

        groupNum = result.group(1)
        monthAd = result.group(2) == '月'
        auditLink = result.group(3) == '审核'

        if not self.isNumber(groupNum):
            return await self.Reply('群编号错误', msgId=msg.id)

        link = createAdLink(groupNum, monthAd, auditLink)
        if link is None:
            return await self.Reply('创建链接失败，请重试', msgId=msg.id)

        content = "公群" + groupNum
        content += "\n%s广告%s(%s天有效)链接\n" % ('月' if monthAd else '', '审核' if auditLink else '', '30' if monthAd else '7')
        content += link

        return await self.Reply(content, msgId=msg.id)

    async def adCheck(self):
        msg = await self.Ask('请输入广告内容')
        if msg is None:
            return await self.Respond('未检测到广告内容')

        await self.Respond('检测中...')

        notifies = []
        if len(msg.text) > 180:
            notifies.append('* 广告内容字数180字符超数')

        sensitiveWords = getSensitiveWords()
        words = []
        for word in sensitiveWords:
            if msg.text.find(word) > -1:
                words.append(word)

        if len(words) > 0:
            notifies.append('* 广告内容出现违禁词“%s”' % ("”, “".join(words)))

        usernames = []
        pattern = r'联系人[：|:]\s*(.*)'
        contact = re.findall(pattern, msg.text)
        if len(contact) > 0:
            pattern = r'\@(\S+)'
            usernames = re.findall(pattern, contact[0])

        groupNum = 0
        pattern = r'公群(\d*)'
        groupNumData = re.findall(pattern, msg.text)
        if len(groupNumData) > 0:
            groupNum = int(groupNumData[0])

        result = checkAds(usernames, groupNum)
        if len(result) > 0:
            for notify in result:
                notifies.append(notify)

        if len(notifies) > 0:
            notifies.append('\n请及时修改。')
            return await self.Reply("\n".join(notifies), msgId=msg.id)
        else:
            return await self.Reply('广告无异常', msgId=msg.id)
