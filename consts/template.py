from hydrogram.types import InlineKeyboardButton

import consts

BtnWelcome = [
    [
        InlineKeyboardButton(text="客户板块", callback_data=consts.callback_data.CallBackCustomer),
        InlineKeyboardButton(text="解禁服务", callback_data=consts.callback_data.CallBackUnblock),
    ]
]

BtnCommonGroup = [
    [
        InlineKeyboardButton(text="查看客服备用群", callback_data=consts.callback_data.CallBackCommonGroupBackup),
        InlineKeyboardButton(text="查询群组状态", callback_data=consts.callback_data.CallBackCommonGroupQueryStatus),
        InlineKeyboardButton(text="修改群名", callback_data=consts.callback_data.CallBackCommonGroupModifyTitle),
    ]
]
