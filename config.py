#==========Библиотеки==========#

#pip install aiogram==2.25.1
#pip install pydantic_settings
#pip install beautifulsoup4
#pip install requests

#==============================#


import logging
import asyncio
import requests
import json
from bs4 import BeautifulSoup as BS
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext




from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


storage = MemoryStorage()

class Settings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()

logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot, storage=storage)
