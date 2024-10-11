import logging
import sys
from logging.handlers import TimedRotatingFileHandler

from hydrogram import Client, filters, enums

import consts
from config import *
from handler import PrivateHandler
from handler.callback import CallbackHandler
from libs.daemon import Daemon

formatter = logging.Formatter(fmt=logFormat, datefmt=logDateFormat)

logger = logging.getLogger()
logger.setLevel(logLevel)

time_handler = TimedRotatingFileHandler(filename=logFile, when='D', interval=1, backupCount=7)
time_handler.setLevel(logLevel)
time_handler.setFormatter(formatter)
logger.addHandler(time_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class BotService(Daemon):
    def run(self):
        api_id = 23896125
        api_hash = "f645cfc0b8d47b9c1d0395d72b3c24db"
        bot_token = botToken

        app = Client(
            "kfzl",
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            parse_mode=enums.ParseMode.DEFAULT,
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
            else:
                await handler.Respond(consts.TextNotKefu)

            data.stop_propagation()

        @app.on_callback_query()
        async def callback(client, data):
            handler = CallbackHandler(client=client, data=data, logger=logger)
            if handler.IsCallback(consts.CallBackCustomer):
                await handler.Customer()
            if handler.IsCallback(consts.CallBackUnblock):
                await handler.Unblock()
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
