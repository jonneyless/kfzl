import hashlib
import logging

import hydrogram
from hydrogram import Client
from hydrogram.errors import MessageNotModified, MessageIdInvalid
from hydrogram.parser.markdown import Markdown
from hydrogram.types import CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup
from hydrogram.types.messages_and_media import message

from config import config
from database.service import checkIsKefu


class BaseHandler():
    def __init__(self, client: Client, data: message.Message | CallbackQuery, logger: logging):
        self.client = client
        self.logger = logger
        self.oData = data
        self.text = None

        if isinstance(data, message.Message):
            self.isCallback = False
            self.msg = data
            self.sender = data.from_user
            self.query = None
            self.text = data.text
        else:
            self.isCallback = True
            if data.message.reply_to_message_id is not None and data.message.reply_to_message_id > 0:
                self.msg = data.message.reply_to_message
            else:
                self.msg = data.message
            self.sender = data.from_user
            self.query = data
            self.data = data.data

        self.chatId = self.msg.chat.id

    def IsKefu(self) -> bool:
        return checkIsKefu(self.sender.id)

    # 判断是否为命令
    def IsCommand(self, command, startswith=False) -> bool:
        if startswith:
            return self.text.startswith(command)

        return self.msg.text.lstrip('/') == command

    # 判断是否为命令
    def IsCallback(self, data, startswith=False) -> bool:
        if startswith:
            return self.data.startswith(data)

        return self.data == data

    # 判断是否为回复信息
    def IsReply(self) -> bool:
        if self.msg.reply_to_message_id is None:
            return False
        return self.msg.reply_to_message_id > 0

    # 获取信息发送人
    def Sender(self):
        return self.sender

    # 获取信息发送人ID
    def SenderId(self):
        return self.sender.id

    # 获取信息发送人ID的字符串类型数据
    def SenderIdString(self):
        return str(self.sender.id)

    # 获取信息发送人Username
    def SenderUsername(self):
        if self.sender.username is not None:
            return self.sender.username

        return str(self.sender.id)

    # 清理上一个消息
    async def CleanPreviousMessage(self):
        return await self.Delete(self.msg.id)

    # 修改上一个消息
    async def EditPreviousMessage(self, content):
        return await self.Edit(self.msg.id, content)

    # 清理问题
    async def CleanAskMessage(self, msg):
        return await self.Delete([msg.id, msg.sent_message.id])

    # 给当前用户发送消息
    async def Respond(self, content, replyMarkup=None, inlineMarkup=True, DisableWebPagePreview=False):
        if replyMarkup is not None:
            if inlineMarkup:
                replyMarkup = InlineKeyboardMarkup(inline_keyboard=replyMarkup)
            else:
                replyMarkup = ReplyKeyboardMarkup(keyboard=replyMarkup)
        return await self.client.send_message(chat_id=self.chatId, text=content, reply_markup=replyMarkup, disable_web_page_preview=DisableWebPagePreview)

    # 删除消息
    async def Delete(self, msgId):
        return await self.client.delete_messages(chat_id=self.chatId, message_ids=msgId)

    # 回复当前用户
    async def Reply(self, content, replyMarkup=None, msgId=None):
        if msgId is None:
            msgId = self.msg.id

        if replyMarkup is not None:
            replyMarkup = InlineKeyboardMarkup(inline_keyboard=replyMarkup)

        return await self.client.send_message(chat_id=self.chatId, text=content, reply_to_message_id=msgId, reply_markup=replyMarkup, disable_web_page_preview=True)

    # 编辑当前用户的消息
    async def Edit(self, msgId, content=None, replyMarkup=None, isMedia=False):
        if replyMarkup is not None:
            replyMarkup = InlineKeyboardMarkup(inline_keyboard=replyMarkup)

        try:
            if content is None and replyMarkup is not None:
                return await self.client.edit_message_reply_markup(chat_id=self.chatId, message_id=int(msgId), reply_markup=replyMarkup)

            if isMedia:
                return await self.client.edit_message_caption(chat_id=self.chatId, message_id=int(msgId), caption=content, reply_markup=replyMarkup)
            else:
                return await self.client.edit_message_text(chat_id=self.chatId, message_id=int(msgId), text=content, reply_markup=replyMarkup)
        except MessageNotModified:
            pass
        except MessageIdInvalid:
            pass

    # 询问当前用户并获取回答
    async def Ask(self, content):
        try:
            return await self.client.ask(chat_id=self.chatId, text=content, user_id=self.sender.id, timeout=60)
        except hydrogram.errors.pyromod.listener_timeout.ListenerTimeout:
            pass

    async def Alert(self, content):
        if self.query is None:
            return

        try:
            await self.query.answer(content, show_alert=True)
        except hydrogram.errors.exceptions.bad_request_400.QueryIdInvalid:
            pass

    # 反解析信息文本的格式
    def GetUnparseText(self, msg: message.Message) -> str:
        if msg.media is not None:
            text = msg.caption
            if msg.caption_entities is not None:
                text = Markdown(self.client).unparse(text, msg.caption_entities)
        else:
            text = msg.text
            if msg.entities is not None:
                text = Markdown(self.client).unparse(text, msg.entities)

        return text

    def isNumber(self, text: str) -> bool:
        if text is None:
            return False

        try:
            float(text)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(text)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # 安全码加盐Hash
    def HashSafeCode(self, code):
        sha256 = hashlib.sha256()
        sha256.update((str(code) + config.md5salt).encode('utf-8'))
        return sha256.hexdigest()
