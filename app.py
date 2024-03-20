import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from settings import settings

import handlers.common as common
import handlers.client as client
import handlers.admin as admin


async def main():
    bot = Bot(settings.bot_token)
    dp = Dispatcher()
    dp.include_routers(common.router, client.router, admin.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())