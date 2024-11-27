import asyncio
import logging

from database.database import database

from handlers import private_router

from bot_config import bot, dp, database

async def on_startup():
    database.create_tables()

async def main():
    dp.include_router(private_router)

    dp.startup.register(on_startup)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())