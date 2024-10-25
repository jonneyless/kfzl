from hydrogram.types import InlineKeyboardButton

import consts

BtnWelcome = [
    [
        InlineKeyboardButton(text="客户板块", callback_data=consts.callback_data.CallBackCustomer),
        InlineKeyboardButton(text="解禁服务", callback_data=consts.callback_data.CallBackUnblock),
    ]
]

BtnAd = [
    [
        InlineKeyboardButton(text="获取广告链接", callback_data=consts.callback_data.CallBackAdGetLink),
        InlineKeyboardButton(text="检测广告内容", callback_data=consts.callback_data.CallBackAdCheck),
    ]
]

BtnCommonGroup = [
    [
        InlineKeyboardButton(text="查看客服备用群", callback_data=consts.callback_data.CallBackCommonGroupBackup),
        InlineKeyboardButton(text="查询群组状态", callback_data=consts.callback_data.CallBackCommonGroupQueryStatus),
        InlineKeyboardButton(text="修改群名", callback_data=consts.callback_data.CallBackCommonGroupModifyTitle),
    ]
]
