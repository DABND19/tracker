from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
DEBUG = env.bool("DEBUG")

with env.prefixed("DB_"):
    DB_HOST = env.str("HOST")
    DB_PORT = env.int("PORT")
    DB_NAME = env.str("NAME")
    DB_USER = env.str("USER")
    DB_PASSWORD = env.str("PASSWORD")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" if not DEBUG \
         else "sqliate+aiosqlite:///database.db"
