import logging
import re
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.register_state import RegisterState
from utils.db_api.pysql import Register

db = Register()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegisterState.fullname)
async def register_user(message: types.Message, state: FSMContext):
    TEXT_FORMAT = "^([A-Z]([a-z']+|\.)\s*){2,3}$"
    if re.match(TEXT_FORMAT, message.text):
        await message.answer('Ismingiz qabul qilindi!\n'
                             'Telefon nomeringizni kiriting!')

        # FSMContext da fullname'ni saqlab ketish
        async with state.proxy() as data:
            data['fullname'] = message.text

        await RegisterState.phone_number.set()
    else:
        await message.answer(
            "Bu ism qabul qilinmadi!\nIsm familya to'liq kiriting va ism kiritganda Kiril alifbodan foydalanmang:")


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=RegisterState.phone_number)
@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=RegisterState.phone_number)
async def register_phone(message: types.Message, state: FSMContext):
    PHONE_NUMBER_FORMAT = "^\+998\d{9}$"

    if message.contact:
        await message.answer("Telefon raqam qabul qilindi!\nLokatsiyani yuboring!")

        async with state.proxy() as data:
            data['phone_number'] = message.text

        await RegisterState.location.set()

    elif re.match(PHONE_NUMBER_FORMAT, message.text):
        await message.answer("Telefon raqam qabul qilindi!\nLokatsiyani yuboring!")

        async with state.proxy() as data:
            data['phone_number'] = message.text

        await RegisterState.location.set()

    else:
        await message.answer("Siz yozgan raqam afsuski mos kelmadi!\Iltimos qaytadan urinib ko'ring:")


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=RegisterState.location)
async def register_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    await message.answer("Sizning ro'yxatdan muvaffaqqiyatli o'tdingiz!")
    async with state.proxy() as data:
        fullname = data['fullname']
        phone_number = data['phone_number']
        language = data['language']

    db.insert(chat_id=message.chat.id, fullname=fullname, phone_number=phone_number, lat=lat, lon=lon, lang=language)
    await state.finish()
