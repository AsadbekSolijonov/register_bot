import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.buttons import InlineBtn
from loader import dp
from states.register_state import RegisterState

in_btn = InlineBtn()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!\n\n"
                         f"Iltimos tilni tanlang", reply_markup=in_btn.languages)
    await RegisterState.language.set()


# @dp.callback_query_handler(lambda cl: cl.data in ["uz", "ru", "en"], state=RegisterState.language)
@dp.callback_query_handler(text=['uz', 'ru', 'en'], state=RegisterState.language)
async def call_lang(call: types.CallbackQuery, state: FSMContext):
    logging.info('Hello')
    async with state.proxy() as data:
        data['language'] = call.data
    await call.message.answer("Ro'yxatdan o'tish uchun to'liq ism familyangizni kriting!")
    await RegisterState.fullname.set()
