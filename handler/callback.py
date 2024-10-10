from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config
import consts
from database.service import GetBossGroupsByTgId, GetBossGroupCountByTgId, NewAllianceGroup, GetBusinessCache, GetAllianceGroupsById, NewGroupBossPwd, NewAlliance, GetUserByTgId
from handler.base import BaseHandler


class CallbackHandler(BaseHandler):
    async def Start(self):
        groups = GetBossGroupsByTgId(self.SenderId())

        content = consts.TextStart
        index = 1
        for group in groups:
            content = content + str(index) + ". " + group.listData() + "\n"
            index = index + 1

        await self.Edit(self.msg.id, content, InlineKeyboardMarkup(inline_keyboard=consts.BtnWelcome))
