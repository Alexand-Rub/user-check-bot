from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db import init_db, get_table

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    init_db()
    await message.answer(
        text='Бот готов к работе!'
    )
    await message.answer(
        text='/chats - Показать список чатов\n/participation - Проверить наличие пользователей'
    )


@router.message(Command("help"))
async def cmd_help(message: Message):


    await message.answer(
        text='/chats - Показать список чатов\n/participation - Проверить наличие пользователей'
    )

