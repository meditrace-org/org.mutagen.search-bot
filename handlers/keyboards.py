from aiogram.types import (ReplyKeyboardMarkup,
                           InlineKeyboardMarkup,
                           KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Найти видео", callback_data="search")
    kb.button(text="Загрузить видео в индекс", callback_data="upload")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def score_kb() -> ReplyKeyboardMarkup:

    kb = [[KeyboardButton(text=f"{i}") for i in range(1, 6)],
          [KeyboardButton(text=f"{i}") for i in range(6, 11)]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Оцени релевантность от 1 до 10",
        one_time_keyboard=True
    )

    return keyboard
