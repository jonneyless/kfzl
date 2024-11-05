from hydrogram.types import InlineKeyboardButton, KeyboardButton

from consts import CallBackCustomer, CallBackUnblock, CallBackUnblockQuery, CallBackSetBlock, CallBackAdGetLink, CallBackAdCheck, CallBackCommonGroupBackup, CallBackCommonGroupQueryStatus, CallBackCommonGroupModifyTitle

UnblockButtons = [
    {'text': '解开骗子库', 'number': 1},
    {'text': '解开黑名单', 'number': 2},
    {'text': '解开 daqun', 'number': 4},
    {'text': '解开 huione888', 'number': 8},
    {'text': '解开 vip', 'number': 16},
    {'text': '解开公群禁言', 'number': 32},
    {'text': '解开公群屏蔽', 'number': 64},
]

BtnWelcome = [
    [
        KeyboardButton(text="客户"),
        KeyboardButton(text="广告"),
        KeyboardButton(text="公群"),
    ],
]

BtnCustomer = [
    [
        InlineKeyboardButton(text="客户板块", callback_data=CallBackCustomer),
        InlineKeyboardButton(text="解禁服务", callback_data=CallBackUnblock),
    ],
    [
        InlineKeyboardButton(text="解禁查询", callback_data=CallBackUnblockQuery),
        InlineKeyboardButton(text="添加封禁", callback_data=CallBackSetBlock),
    ]
]

BtnAd = [
    [
        InlineKeyboardButton(text="获取广告链接", callback_data=CallBackAdGetLink),
        InlineKeyboardButton(text="检测广告内容", callback_data=CallBackAdCheck),
    ]
]

BtnSetBlock = [
    [
        InlineKeyboardButton(text="tgId", callback_data=CallBackSetBlock + ':1'),
        InlineKeyboardButton(text="用户名", callback_data=CallBackSetBlock + ':2'),
    ]
]

BtnCommonGroup = [
    [
        InlineKeyboardButton(text="查看客服备用群", callback_data=CallBackCommonGroupBackup),
        InlineKeyboardButton(text="查询群组状态", callback_data=CallBackCommonGroupQueryStatus),
        InlineKeyboardButton(text="修改群名", callback_data=CallBackCommonGroupModifyTitle),
    ]
]
