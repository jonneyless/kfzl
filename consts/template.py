from hydrogram.types import InlineKeyboardButton

import consts

TextStart = "🏠 你好！\n\n欢迎使用**客服助理机器人**"
TextNotKefu = "对不起，你不是汇旺客服人员"

BtnWelcome = [
    [
        InlineKeyboardButton(text="客户板块", callback_data=consts.callback_data.CallBackCustomer),
        InlineKeyboardButton(text="解禁服务", callback_data=consts.callback_data.CallBackUnblock),
    ]
]
