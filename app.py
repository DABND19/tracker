from aiogram import executor
from models import Base
from loader import engine, Session, dp, chats_store
import filters, handlers


async def on_startup(*args):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with Session() as session:
        await chats_store.load(session)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
