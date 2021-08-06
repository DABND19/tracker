from aiogram import executor
from models import metadata
from loader import engine, Session, dp, chats_store


async def on_startup():
    with Session() as session:
        await session.run_sync(metadata.create_all(engine))
        await chats_store.load(session)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
