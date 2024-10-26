import json

from hydrogram.types import InlineKeyboardButton

from consts import UnblockButtons, CallBackUnblockConfirm, CallBackSetBlockConfirm, CallBackUnblock, CallBackCancel
from database.service import getFrom, getKefu, getUnCheatCount, getUnBlackCount, NewUnblockRecord, getUnblockRecords
from handler.ad import AdHandler
from handler.base import BaseHandler
from handler.group import GroupHandler
from libs.helper import getUserCheat, getUserBlack, userUnCheat, userUnBlack, getUserInfo, buildUnblockButton, userUnban, userGQUnban, formatDatetime, setBlack, setCheat, checkOfficial
from libs.logger import logger


class CallbackHandler(BaseHandler):

    def group(self):
        return GroupHandler(client=self.client, data=self.oData, logger=self.logger)

    def ad(self):
        return AdHandler(client=self.client, data=self.oData, logger=self.logger)

    async def Customer(self):
        await self.CleanPreviousMessage()

        msg = await self.askUser()
        if msg is not None:
            userId = msg.text

            await self.CleanAskMessage(msg)

            user = getFrom(userId)
            if user is None:
                return await self.Respond('用户“%s”不存在' % userId)

            kefuNickname = ''
            kefuName = ''
            kefu = getKefu(user.user_id)
            if kefu is not None:
                kefuNickname = kefu.nickname
                kefuName = kefu.name

            return await self.Respond("tgId：<code>%s</code>\n用户名：@<code>%s</code>\n所属客服：%s %s" % (user.user_tg_id, user.username, kefuNickname, kefuName))

    async def Unblock(self):
        data = self.data.split(":")
        userId = None
        selected = 0
        status = []
        dataLen = len(data)
        isEdit = False
        if dataLen > 1:
            userId = data[1]

            if dataLen > 2:
                selected = int(data[2])
                status = data[3].split(",")
                isEdit = True
        else:
            await self.CleanPreviousMessage()

        loading = None
        content = None

        if userId is None:
            msg = await self.askUser()
            if msg is None:
                return

            await self.CleanAskMessage(msg)

            userId = msg.text

        if not isEdit:
            loading = await self.Respond('正在查询，请稍等...')

            content = "客户的状态如下：\n"
            content += "tgId：<code>%s</code>\n" % userId

            user = getFrom(userId)
            if user is not None:
                content += "用户名：@<code>%s</code>\n" % user.username

            content += '解黑名单次数：%s\n' % getUnBlackCount(userId)
            content += '解骗子库次数：%s\n' % getUnCheatCount(userId)

            cheat = getUserCheat(userId)
            if cheat is not None and cheat['flag'] == 1:
                content += "骗子库：是，%s, %s\n" % (cheat['reason'], cheat['ope_user'])
                status.append('1')
            else:
                content += "骗子库：否\n"
                status.append('0')

            black = getUserBlack(userId)
            if black is not None and black['flag'] == 1:
                content += "黑名单：是，%s, %s\n" % (black['reason'], black['ope_user'])
                status.append('1')
            else:
                content += "黑名单：否\n"
                status.append('0')

            userInfo = getUserInfo(userId)
            if userInfo is not None:
                if 'daqun' in userInfo:
                    if userInfo['daqun']['is_restricted'] == 1:
                        content += "大群 @daqun 禁言：是\n"
                    else:
                        content += "大群 @daqun 禁言：否\n"

                    if userInfo['daqun']['is_baned'] == 1:
                        content += "大群 @daqun 屏蔽：是\n"
                    else:
                        content += "大群 @daqun 屏蔽：否\n"

                    if userInfo['daqun']['is_restricted'] == 1 or userInfo['daqun']['is_baned'] == 1:
                        status.append('1')
                    else:
                        status.append('0')

                if 'huione888' in userInfo:
                    if userInfo['huione888']['is_restricted'] == 1:
                        content += "大群 @huione888 禁言：是\n"
                    else:
                        content += "大群 @huione888 禁言：否\n"

                    if userInfo['huione888']['is_baned'] == 1:
                        content += "大群 @huione888 屏蔽：是\n"
                    else:
                        content += "大群 @huione888 屏蔽：否\n"

                    if userInfo['huione888']['is_restricted'] == 1 or userInfo['huione888']['is_baned'] == 1:
                        status.append('1')
                    else:
                        status.append('0')

                if 'vip' in userInfo:
                    if userInfo['vip']['is_restricted'] == 1:
                        content += "VIP禁言：是\n"
                    else:
                        content += "VIP禁言：否\n"

                    if userInfo['vip']['is_baned'] == 1:
                        content += "VIP屏蔽：是\n"
                    else:
                        content += "VIP屏蔽：否\n"

                    if userInfo['vip']['is_restricted'] == 1 or userInfo['vip']['is_baned'] == 1:
                        status.append('1')
                    else:
                        status.append('0')

                if 'gongqun' in userInfo:
                    if userInfo['vip']['is_restricted'] == 1:
                        content += "公群禁言：是\n"
                        status.append('1')
                    else:
                        content += "公群禁言：否\n"
                        status.append('0')

        buttons = []
        selectAll = 0
        for i in range(len(UnblockButtons)):
            if status[i] == '1':
                selectAll = selectAll | UnblockButtons[i]['number']
                buttons.append(buildUnblockButton(UnblockButtons[i]['text'], userId, selected, UnblockButtons[i]['number'], status))

        rows = []
        rowButtons = []
        if len(buttons) > 0:
            for button in buttons:
                rowButtons.append(button)

                if len(rowButtons) == 2:
                    rows.append(rowButtons)
                    rowButtons = []

            if len(rowButtons) > 0:
                rows.append(rowButtons)

            rowButtons = [
                InlineKeyboardButton(text='确定', callback_data=CallBackUnblockConfirm + ':' + userId + ':' + str(selected))
            ]

        rowButtons.append(InlineKeyboardButton(text="关闭", callback_data=CallBackCancel))
        rows.append(rowButtons)

        if not isEdit:
            if loading is not None:
                return await self.Edit(loading.id, content, replyMarkup=rows)
            else:
                return await self.Respond(content, replyMarkup=rows)
        else:
            return await self.Edit(self.msg.id, replyMarkup=rows)

    async def UnblockConfirm(self):
        data = self.data.split(":")
        userId = data[1]
        selected = int(data[2])

        user = getFrom(userId)
        name = userId
        if user is not None:
            name = '@' + user.username

        await self.Edit(self.msg.id, content=self.msg.text)

        content = '开始处理 %s，请等待...\n' % name
        msg = await self.Respond(content)

        if (selected & 1) == 1:
            content += '\n移出骗子库：'
            if not userUnCheat(userId):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

        if (selected & 2) == 2:
            content += '\n移出黑名单：'
            if not userUnBlack(userId):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

        if (selected & 4) == 4:
            content += '\n@daqun 移除黑名单：'
            if not userUnban(userId, 1, 'daqun'):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

            content += '\n@daqun 解除禁言：'
            if not userUnban(userId, 2, 'daqun'):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

        if (selected & 8) == 8:
            content += '\n@huione888 移除黑名单：'
            if not userUnban(userId, 1, 'huione888'):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

            content += '\n@huione888 解除禁言：'
            if not userUnban(userId, 2, 'huione888'):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

        if (selected & 16) == 16:
            content += '\nVIP 移除黑名单：'
            if not userUnban(userId, 1, 'vip'):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

            content += '\nVIP 解除禁言：'
            if not userUnban(userId, 2, 'vip'):
                content += '失败'
            else:
                content += '成功'

            await msg.edit(content)

        if (selected & 32) == 32:
            content += '\n公群解除禁言：'
            callbackData = {'message_id': msg.id, 'chat_id': self.chatId, 'text': content}
            content += '处理中...'
            await msg.edit(content)

            userGQUnban(userId, json.dumps(callbackData))

        NewUnblockRecord(self.SenderIdString(), self.SenderUsername(), userId, selected)

        await self.Delete(self.msg.id)

        self.data = CallBackUnblock + ':' + userId
        await self.Unblock()

    async def UnblockQuery(self):
        await self.CleanPreviousMessage()

        msg = await self.askUser()
        if msg is not None:
            userId = msg.text

            await self.CleanAskMessage(msg)

            records = getUnblockRecords(userId)
            recordGroup = {
                1: {
                    'title': '骗子库',
                    'data': []
                },
                2: {
                    'title': '黑名单',
                    'data': []
                },
                4: {
                    'title': 'daqun',
                    'data': []
                },
                8: {
                    'title': 'huione888',
                    'data': []
                },
                16: {
                    'title': 'VIP',
                    'data': []
                },
                32: {
                    'title': '公群',
                    'data': []
                },
            }
            for record in records:
                for actType in recordGroup:
                    if (record.type & actType) == actType:
                        recordGroup[actType]['data'].append(record)

            content = "客户解禁记录如下：\n"
            content += "tgId：<code>%s</code>\n" % userId

            user = getFrom(userId)
            if user is not None:
                content += "用户名：@<code>%s</code>\n" % user.username

            for actType in recordGroup:
                if len(recordGroup[actType]['data']) == 0:
                    continue

                content += "\n" + recordGroup[actType]['title'] + "：\n"
                for record in recordGroup[actType]['data']:
                    content += formatDatetime(record.created_at) + ' - 操作人 @' + record.action_name + '\n'

            return await self.Respond(content)

    async def SetBlock(self):
        data = self.data.split(":")
        dataLen = len(data)
        if dataLen == 1:
            await self.CleanPreviousMessage()

            msg = await self.askUser('要封禁')
            if msg is None:
                return await self.Respond('未收到输入的 TgID')

            await self.CleanAskMessage(msg)

            data.append(msg.text)
            dataLen += 1

        tgId = None
        inStatus = 0
        if dataLen > 1:
            tgId = str(data[1])

            if checkOfficial(tgId):
                return await self.Respond('“%s”是官方帐号' % tgId)

            cheat = getUserCheat(tgId)
            if cheat is not None and cheat['flag'] == 1:
                inStatus = inStatus | 1

            black = getUserBlack(tgId)
            if black is not None and black['flag'] == 1:
                inStatus = inStatus | 2

            if inStatus & 1 == 1 and inStatus & 2 == 2:
                return await self.Respond('“%s”已在黑名单和骗子库中' % tgId)

            if dataLen == 2:
                data.append(str(inStatus))
                dataLen += 1

                buttons = []
                if inStatus & 1 != 1:
                    buttons.append(InlineKeyboardButton(text="骗子库", callback_data=':'.join(data) + ':1'))

                if inStatus & 2 != 2:
                    buttons.append(InlineKeyboardButton(text="黑名单", callback_data=':'.join(data) + ':2'))

                buttons.append(InlineKeyboardButton(text="取消", callback_data=CallBackCancel))

                return await self.Respond('请选择要对“%s”进行的处理类型' % tgId, [buttons])

        if dataLen > 2:
            inStatus = int(data[2])
            blockType = int(data[3])
            data.pop()

            buttons = []
            if inStatus & 1 != 1:
                buttons.append(InlineKeyboardButton(text="✅️骗子库" if blockType & 1 == 1 else "️骗子库", callback_data=':'.join(data) + ':' + (str(blockType ^ 1) if blockType & 1 == 1 else str(blockType | 1))))

            if inStatus & 2 != 2:
                buttons.append(InlineKeyboardButton(text="✅️黑名单" if blockType & 2 == 2 else "黑名单", callback_data=':'.join(data) + ':' + (str(blockType ^ 2) if blockType & 2 == 2 else str(blockType | 2))))

            if blockType & 1 == 1 or blockType & 2 == 2:
                buttons.append(InlineKeyboardButton(text="确认", callback_data="%s:%s:%s" % (CallBackSetBlockConfirm, tgId, blockType)))

            buttons.append(InlineKeyboardButton(text="取消", callback_data=CallBackCancel))

            return await self.Edit(self.msg.id, replyMarkup=[buttons])

    async def SetBlockConfirm(self):
        await self.CleanPreviousMessage()

        data = self.data.split(":")

        logger.info("Callback Data: " + json.dumps(data))

        blockTgId = str(data[1])
        blockType = int(data[2])

        content = "请输入封禁原因\n\ntgId: " + blockTgId + '\n'
        content += "类型："
        if blockType & 1 == 1:
            content += "骗子库"
        if blockType & 2 == 2:
            if blockType & 1 == 1:
                content += "、"
            content += "黑名单"

        msg = await self.Ask(content)
        if msg is None:
            return await self.Respond('未收到输入的封禁原因')

        await self.CleanAskMessage(msg)

        if blockType & 1 == 1:
            setCheat(blockTgId, self.SenderIdString(), msg.text)

        if blockType & 2 == 2:
            setBlack(blockTgId, self.SenderIdString(), msg.text)

        content = "完成封禁\n\ntgId: " + blockTgId + '\n'
        content += "类型："
        if blockType & 1 == 1:
            content += "骗子库"
        if blockType & 2 == 2:
            if blockType & 1 == 1:
                content += "、"
            content += "黑名单"
        content += "\n原因：" + msg.text

        return await self.Respond(content)

    async def askUser(self, userType="客户"):
        msg = await self.Ask('请输入%s的tgId' % userType)

        if msg is None:
            await self.CleanAskMessage(msg)
            await self.Alert('未收到%s的tgId' % userType)
        elif not self.isNumber(msg.text):
            await self.CleanAskMessage(msg)
            await self.Alert('输入的tgId不正确')
        else:
            return msg

        return None
