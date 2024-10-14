import re

from hydrogram.types import InlineKeyboardMarkup

import consts
from database.service import getSensitiveWords, getFrom, NewGroupLink
from handler.base import BaseHandler
from libs.helper import checkAds, getUnUsedGroupNum, getUserCheatInfo, getUserSpecialGroup, getUserCommonGroup, createBotApproveLink


class PrivateHandler(BaseHandler):

    async def Welcome(self):
        return await self.Respond(consts.TextStart, InlineKeyboardMarkup(inline_keyboard=consts.BtnWelcome))

    async def Ad(self):
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
        print(contact)
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

    async def GroupNum(self):
        data = getUnUsedGroupNum()
        chunk = []
        for i in range(0, len(data), 400):
            chunk.append(data[i:i + 400])

        for items in chunk:
            await self.Reply(", ".join(map(str, items)))

        await self.Reply("数目： %s" % len(data))

    async def QueryUser(self):
        pattern = r'id (\d+)'
        data = re.findall(pattern, self.text)
        if len(data) > 0:
            userId = data[0]
            user = getFrom(userId)
            if user is None:
                return await self.Reply('用户不存在')

            specialGroup = getUserSpecialGroup(userId)
            commonGroup = getUserCommonGroup(userId)
            cheatInfo = getUserCheatInfo(userId)
            remove_cheat_special_num = 0
            remove_cheat_num = 0
            unban_num = 0
            cancel_restrict_num = 0
            if cheatInfo != []:
                remove_cheat_special_num = cheatInfo['remove_cheat_special_num']
                remove_cheat_num = cheatInfo['remove_cheat_num']
                unban_num = cheatInfo['unban_num']
                cancel_restrict_num = cheatInfo['cancel_restrict_num']

            content = '''
            所在群组：专群 %s 个，公群 %s 个
广告发布次数：%s
上押次数：%s
上押金额：%s
纠纷次数：%s
纠纷次数：%s
仲裁次数：%s
公审次数：%s
解禁次数：%s
解封次数：%s
解黑名单次数：%s
解骗子库次数：%s
            ''' % (specialGroup, commonGroup, 0, user.yajin_num, user.yajin_money, 0, 0, 0, 0, cancel_restrict_num, unban_num, remove_cheat_num, remove_cheat_special_num)
            return await self.Reply(content)

    async def GenLink(self):
        groupTgId = False
        if self.text == "SVIP群":
            groupTgId = "-1001601629727"
        elif self.text == "VIP群":
            groupTgId = "-1001753191368"
        elif self.text == "盘总群":
            groupTgId = "-1001824105782"
        elif self.text == "招聘群":
            groupTgId = "-1001986586516"
        elif self.text == "黑客群":
            groupTgId = "-1001950107503"
        elif self.text == "站长群":
            groupTgId = "-1001910194051"
        elif self.text == "美工/搭建群":
            groupTgId = "-1001821490286"
        elif self.text == "账号群":
            groupTgId = "-1001927554058"
        elif self.text == "test":
            groupTgId = "-1001677560391"

        if not groupTgId:
            return await self.Reply("信息错误")

        link = createBotApproveLink(groupTgId)
        if link is None:
            return await self.Reply("创建链接失败，请重试")

        NewGroupLink(groupTgId, self.SenderId(), link)

        msg = self.text
        msg += "\n单日单人链接\n"
        msg += link

        return await self.Reply(msg)
