from aiogram import Router, F, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f'Привет, {name}!. Вас приветствует Бот для дз для отправки дз используйте команду /dz'
    await message.answer(msg)
