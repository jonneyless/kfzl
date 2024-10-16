from config import notifyGroupId
from handler.base import BaseHandler
from libs.helper import getGroupBackupData, getGroupInfo, setGroupTitle


class GroupHandler(BaseHandler):

    async def Backup(self):
        data = getGroupBackupData()
        if data is None:
            return await self.Respond('对不起，没有数据')

        content = ""
        for datum in data:
            content += "群名：%s\ntgid：%s\n链接：%s\n\n" % (datum['title'], datum['chat_id'], datum['link'])

        return await self.Respond(content)

    async def QueryStatus(self):
        msg = await self.Ask("请输入要查询的群编号")
        if msg is None:
            return await self.Respond("没有收到群编号")

        data = getGroupInfo(msg.text)
        if data is None or "title" not in data:
            return await self.Respond('对不起，没有数据')

        content = "%s\ntgid：%s\n链接：%s\n业务类型：%s\n公群人数：%s人" % (data['title'], data['chat_id'], data['link'], data['business_detail_type'], data['num'])

        return await self.Respond(content)

    async def ModifyTitle(self):
        msg = await self.Ask("请输入群ID")
        if msg is None:
            return await self.Respond("没有收到群ID")
        elif not self.isNumber(msg.text):
            return await self.Respond("群ID输入错误")

        groupId = msg.text

        msg = await self.Ask("请输入新的群名")
        if msg is None:
            return await self.Respond("没有收到群名")

        data = setGroupTitle(groupId, msg.text)
        if 'title_old' not in data:
            return await self.Respond('修改失败，请联系技术')

        content = "tg_id：%s\n旧群名：%s\n新群名：%s" % (groupId, data['title_old'], data['title_new'])

        await self.client.send_message(notifyGroupId, content)

        content = "修改成功\n\n单人单个一小时进群链接：%s" % data['link']

        return await self.Respond(content)
