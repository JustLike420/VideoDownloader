# coding=utf-8
from aiogram.utils import executor
from aiogram.types.update import Update
import handlers
import handlers.commands
import handlers.all_messages
import handlers.callback

from utils.help_functions import on_startup
from main import dp


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
