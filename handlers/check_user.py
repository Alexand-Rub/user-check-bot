import os
from asyncio import sleep
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards.chats import chats, ChatsCallbackFactory
from db import get_users

router = Router()

class UserList(StatesGroup):
    download = State()


@router.message(Command("participation"))
async def cmd_participation(message: Message):
    await message.answer(
        text='Выберете чат для проверки',
        reply_markup=chats()
    )


@router.callback_query(ChatsCallbackFactory.filter())
async def get_chat(callback: CallbackQuery, callback_data: ChatsCallbackFactory, state: FSMContext):
    await state.update_data(chat_id=callback_data.chat_id)
    await callback.message.answer(text='Загрузите список пользователей')
    await state.set_state(UserList.download)
    await callback.answer()


@router.message(UserList.download, F.document)
async def food_chosen(message: Message, state: FSMContext, bot):
    if message.document.file_name.split('.')[1] != 'txt':
        await message.reply(text='Пришлите документ .txt')
    else:
        await bot.download(
            message.document,
            destination="text.txt"
        )
        await message.answer('Подождите...')
        await sleep(2)
        exist = ''
        not_exist = ''
        data = await state.get_data()
        users = get_users(data['chat_id'])
        with open('text.txt') as f:
            for n in f:
                name = n.split('\n')[0]
                if name.split('\n')[0] in users:
                    exist += n
                else:
                    not_exist += n

        await message.answer('Есть в чате: \n{list}'.format(list=exist))
        await message.answer('Нет в чате: \n{list}'.format(list=not_exist))
        os.remove('text.txt')


@router.message(UserList.download)
async def food_chosen(message: Message, state: FSMContext):
    await message.reply(text='Это не докумет. Пришлите документ .TXT')

