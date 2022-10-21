from aiogram import Bot, Dispatcher
from config import bot_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage_memory = MemoryStorage()

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=storage_memory)
