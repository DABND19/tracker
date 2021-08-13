from os import environ


BOT_TOKEN = environ.get("BOT_TOKEN")

DB_USER  = environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD", "123456")
DB_HOST = environ.get("POSTGRES_HOST", "localhost")
DB_PORT = environ.get("POSTGRES_PORT", "5432")
DB_NAME = environ.get("POSTGRES_NAME", "postgres")

REDIS_HOST = environ.get("REDIS_HOST", "localhost")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
