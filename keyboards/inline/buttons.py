from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class InlineBtn:
    @property
    def languages(self):
        btn = InlineKeyboardMarkup(row_width=2)
        uz = InlineKeyboardButton(text='🇺🇿uz', callback_data='uz')
        ru = InlineKeyboardButton(text='🇷🇺ru', callback_data='ru')
        en = InlineKeyboardButton(text='🇺🇸en', callback_data='en')
        btn.add(ru, en, uz)
        return btn


