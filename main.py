import sys

from hydrogram import Client, filters, enums

import consts
from config import *
from handler import PrivateHandler
from handler.callback import CallbackHandler
from libs.daemon import Daemon
from libs.logger import logger


class BotService(Daemon):
    def run(self):
        api_id = appId
        api_hash = appHash
        bot_token = botToken

        app = Client(
            "kfzl",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            parse_mode=enums.ParseMode.HTML,
        )

        @app.on_message(filters.private)
        async def private(client, data):
            handler = PrivateHandler(client=client, data=data, logger=logger)

            if handler.IsKefu():
                if handler.IsCommand(consts.CmdStart):
                    await handler.Welcome()
                elif handler.IsCommand(consts.CmdAd):
                    await handler.Ad()
                elif handler.IsCommand(consts.CmdNotInUseGroupNum):
                    await handler.GroupNum()
                elif handler.IsCommand(consts.CmdQueryUser, True):
                    await handler.QueryUser()
                elif handler.IsCommand(consts.CmdCommonGroup):
                    await handler.CommonGroup()
                else:
                    await handler.GenLink()
            else:
                await handler.Respond("对不起，你不是汇旺客服人员")

            data.stop_propagation()

        @app.on_callback_query()
        async def callback(client, data):
            handler = CallbackHandler(client=client, data=data, logger=logger)
            if handler.IsCallback(consts.CallBackCustomer):
                await handler.Customer()
            if handler.IsCallback(consts.CallBackUnblock):
                await handler.Unblock()
            if handler.IsCallback(consts.CallBackUnCheat, True):
                await handler.UnCheat()
            if handler.IsCallback(consts.CallBackUnBlack, True):
                await handler.UnBlack()
            if handler.IsCallback(consts.CallBackCommonGroupBackup):
                await handler.group.Backup()
            if handler.IsCallback(consts.CallBackCommonGroupQueryStatus):
                await handler.group.QueryStatus()
            if handler.IsCallback(consts.CallBackCommonGroupModifyTitle):
                await handler.group.ModifyTitle()
            if handler.IsCallback(consts.CallBackCommonGroupModifyConfirm, True):
                await handler.group.ModifyConfirm()
            if handler.IsCallback(consts.CallBackAdGetLink):
                await handler.adLink()
            if handler.IsCallback(consts.CallBackAdCheck):
                await handler.adCheck()
            if handler.IsCallback(consts.CallBackCancel):
                await handler.Delete(handler.msg.id)
            data.stop_propagation()

        app.run()


botService = BotService("runtime/service.pid")

if len(sys.argv) > 1:
    command = sys.argv[1]
    match command:
        case "start":
            botService.start()
        case "stop":
            botService.stop()
        case "restart":
            botService.restart()
        case "status":
            botService.status()
        case _:
            botService.run()
else:
    botService.run()
