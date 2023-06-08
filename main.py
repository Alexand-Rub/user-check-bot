import asyncio
from aiogram import Bot, Dispatcher
from handlers import common, check_user, add_bot, add_user

from config_reader import config


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        common.router,
        check_user.router,
        add_user.router,
        add_bot.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
