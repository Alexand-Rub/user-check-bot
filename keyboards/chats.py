from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import get_table


class ChatsCallbackFactory(CallbackData, prefix="chat"):
    chat_id: int


def chats() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for chat in get_table(table='chats'):
        kb.button(
            text=chat[1],
            callback_data=ChatsCallbackFactory(chat_id=chat[0])

        )
    return kb.as_markup(resize_keyboard=True)

