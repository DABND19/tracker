from aiogram import executor
from models import Base
from loader import engine, Session, dp, chats_store, bot
import filters
import handlers
import logging
from data.config import WEBHOOK_URL


logging.basicConfig(level=logging.INFO)


async def on_startup(*args):
    await bot.set_webhook(WEBHOOK_URL)
    
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with Session() as session:
        await chats_store.load(session)


if __name__ == "__main__":
    executor.start_webhook(
        dispatcher=dp,
        on_startup=on_startup,
        skip_updates=True,
        webhook_path="/",
        host="localhost",
        port=3001
    )
