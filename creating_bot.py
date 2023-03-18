from aiogram import Bot, Dispatcher
import logging
from config_reader import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="MarkdownV2")
dp = Dispatcher()