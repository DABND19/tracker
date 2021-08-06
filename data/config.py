from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.read_env("BOT_TOKEN")
