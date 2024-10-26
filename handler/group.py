from hydrogram.types import InlineKeyboardButton

from consts import CallBackCancel, CallBackCommonGroupModifyConfirm
from handler.base import BaseHandler
from libs.api import sendNotification
from libs.helper import getGroupBackupData, getGroupInfo, setGroupTitle


class GroupHandler(BaseHandler):

    async def Backup(self):
        await self.CleanPreviousMessage()

        data = getGroupBackupData()
        if data is None:
            return await self.Respond('对不起，没有数据')

        content = ""
        for datum in data:
            content += "群名：%s\ntgid：<code>%s</code>\n链接：%s\n\n" % (datum['title'], datum['chat_id'], datum['link'])

        return await self.Respond(content)

    async def QueryStatus(self):
        await self.CleanPreviousMessage()

        msg = await self.Ask("请输入要查询状态的群编号，格式 “公群123”")
        if msg is None:
            return await self.Respond("没有收到群编号")

        title = msg.text
        data = getGroupInfo(title)

        await self.CleanAskMessage(msg)

        if data is None or "title" not in data:
            return await self.Respond('对不起，没有找到 “%s” 的相关状态数据' % title)

        content = "%s\ntgid：<code>%s</code>\n链接：%s\n业务类型：%s\n公群人数：%s人" % (data['title'], data['chat_id'], data['link'], data['business_detail_type'], data['num'])

        return await self.Respond(content)

    async def ModifyTitle(self):
        await self.CleanPreviousMessage()

        msg = await self.Ask("请输入要修改群名的群ID")
        if msg is None:
            return await self.Respond("没有收到群ID")
        elif not self.isNumber(msg.text):
            return await self.Respond("群ID输入错误")

        groupId = msg.text

        await self.CleanAskMessage(msg)

        msg = await self.Ask("请输入ID “%s” 的新群名" % groupId)
        if msg is None:
            return await self.Respond("没有收到群名")

        await self.Respond('请确认ID “%s” 新的群名：\n\n' % groupId + msg.text, [
            [
                InlineKeyboardButton(text="确认", callback_data=CallBackCommonGroupModifyConfirm + ':' + groupId + ':' + str(msg.id) + ':' + str(msg.sent_message.id)),
                InlineKeyboardButton(text="取消", callback_data=CallBackCancel),
            ]
        ])

    async def ModifyConfirm(self):
        data = self.data.split(':')
        groupId = data[3]
        msgId = int(data[4])
        askMsgId = int(data[5])

        msg = await self.client.get_messages(self.chatId, msgId)

        await self.CleanPreviousMessage()
        await self.Delete([msgId, askMsgId])

        data = setGroupTitle(groupId, msg.text, msg.from_user.id, msg.from_user.username, msg.from_user.full_name)

        if data is None or 'title_old' not in data:
            return await self.Respond('ID “%s” 群名修改失败，请联系技术' % groupId)

        content = "tg_id：%s\n旧群名：%s\n新群名：%s" % (groupId, data['title_old'], data['title_new'])

        sendNotification(content)

        content = "ID “%s” 群名修改成功\n\n单人单个一小时进群链接：%s" % (groupId, data['link'])

        return await self.Respond(content)
