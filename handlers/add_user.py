from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import ChatMemberUpdated

from filters.chat_type import ChatTypeFilter
from db import add_user, delete_user, get_table

router = Router()


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def new_user_add(event: ChatMemberUpdated):
    add_user(
        user_id=event.new_chat_member.user.id,
        chat_id=event.chat.id,
        user_name=event.new_chat_member.user.username
    )


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER >> IS_NOT_MEMBER))
async def user_deleted(event: ChatMemberUpdated):
    delete_user(
        user_id=event.new_chat_member.user.id,
        chat_id=event.chat.id
    )


@router.message(ChatTypeFilter(chat_type=["group", "supergroup"]))
async def old_user_add(message: Message):
    if message.from_user.id not in list(set([int(i[0]) for i in get_table(table='users')])):
        add_user(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            user_name=message.from_user.username
        )