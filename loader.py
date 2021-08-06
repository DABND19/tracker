from aiogram import Bot, Dispatcher
from data.config import BOT_TOKEN
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from data.chats import ChatsStore


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

engine = create_async_engine("sqlite+aiosqlite:///database.db")
Session = sessionmaker(bind=engine, class_=AsyncSession)

chats_store = ChatsStore()
