import re

from hydrogram.types import InlineKeyboardMarkup

import consts
from database.service import getSensitiveWords, getFrom
from handler.base import BaseHandler
from libs.helper import checkAds, getUnUsedGroupNum, getUserCheatInfo, getUserSpecialGroup, getUserCommonGroup


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
            return await msg.reply("\n".join(notifies))
        else:
            return await msg.reply('广告无异常')

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
            ''' % (specialGroup, commonGroup, 0, user['yajin_num'], user['yajin_money'], 0, 0, 0, cancel_restrict_num, unban_num, remove_cheat_num, remove_cheat_special_num)
            return await self.Reply(content)
