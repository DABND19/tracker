# from environs import Env
from os import environ

# env = Env()
# env.read_env()

# BOT_TOKEN = env.str("BOT_TOKEN")
# DEBUG = env.bool("DEBUG")

# with env.prefixed("DB_"):
#     DB_HOST = env.str("HOST")
#     DB_PORT = env.int("PORT")
#     DB_NAME = env.str("NAME")
#     DB_USER = env.str("USER")
#     DB_PASSWORD = env.str("PASSWORD")

BOT_TOKEN = environ.get("BOT_TOKEN")
DEBUG = False

DB_USER  = environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD", "123456")
DB_HOST = environ.get("POSTGRES_HOST", "localhost")
DB_PORT = environ.get("POSTGRES_PORT", "5432")
DB_NAME = environ.get("POSTGRES_DB", "postgres")

REDIS_HOST = environ.get("REDIS_HOST", "localhost")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" if not DEBUG \
         else "sqlite+aiosqlite:///database.db"

# with env.prefixed("REDIS_"):
#     REDIS_HOST = env.str("HOST")
#     # REDIS_PORT = env.int("PORT")
#     # REDIS_DB = env.str("DB")
#     # REDIS_PASSWORD = env.str("PASSWORD")
