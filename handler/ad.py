import re

from database.service import getSensitiveWords
from handler.base import BaseHandler
from libs.helper import createAdLink, checkAds


class AdHandler(BaseHandler):

    async def adLink(self):
        await self.CleanPreviousMessage()

        msg = await self.Ask('请输入获取广告链接指令')
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

        link, title = createAdLink(groupNum, monthAd, auditLink)
        if link is None:
            return await self.Reply('创建链接失败，请重试', msgId=msg.id)

        content = title
        content += "\n%s广告%s(%s天有效)链接\n" % ('月' if monthAd else '', '审核' if auditLink else '', '30' if monthAd else '7')
        content += link

        return await self.Reply(content, msgId=msg.id)

    async def adCheck(self):
        await self.CleanPreviousMessage()

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
        pattern = r'公群(\d+)'
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
