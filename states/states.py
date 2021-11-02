# - *- coding: utf- 8 - *-
from aiogram.dispatcher.filters.state import State, StatesGroup


class VideoResolution(StatesGroup):
    data = State()
