from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command

from bot_config import database

hw_dialog_router = Router()

class HwDialog(StatesGroup):
    name = State()
    group = State()
    hw_number = State()
    git_rep = State()

@hw_dialog_router.message(Command("dz"))
async def start_dz(message: types.Message, state: FSMContext):
    await state.set_state(HwDialog.name)
    await message.answer("Как вас зовут?")

@hw_dialog_router.message(HwDialog.name)
async def process_name(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await message.answer("Имя должно содержать только буквы. Попробуйте снова.")
        return
    await state.update_data(name=message.text)
    await state.set_state(HwDialog.group)
    kbgroup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f'group_{i}') for i in range(1, 4)]
        ]
    )
    await message.answer("Какая группа?", reply_markup=kbgroup)

@hw_dialog_router.callback_query(HwDialog.group, F.data.startswith('group_'))
async def process_group(callback_query: types.CallbackQuery, state: FSMContext):
    group_name = callback_query.data.split('_')[1]
    if not group_name.isdigit():
        await callback_query.message.answer("Некорректный выбор группы. Попробуйте снова.")
        return
    await state.update_data(group=group_name)
    await state.set_state(HwDialog.hw_number)
    await callback_query.answer()
    kbhw = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f'hw_{i}') for i in range(1, 9)]
        ]
    )
    await callback_query.message.answer("Номер дз?", reply_markup=kbhw)

@hw_dialog_router.callback_query(HwDialog.hw_number, F.data.startswith('hw_'))
async def process_hw(callback_query: types.CallbackQuery, state: FSMContext):
    hw_number = callback_query.data.split('_')[1]
    if not hw_number.isdigit():
        await callback_query.message.answer("Некорректный выбор номера ДЗ. Попробуйте снова.")
        return
    await state.update_data(hw_num=hw_number)
    await state.set_state(HwDialog.git_rep)
    await callback_query.answer()
    await callback_query.message.answer("Введите ссылку на репозиторий:")

@hw_dialog_router.message(HwDialog.git_rep)
async def process_git_rep(message: types.Message, state: FSMContext):
    if not message.text.startswith("https://github.com"):
        await message.answer("Ссылка должна начинаться с 'https://github.com'. Попробуйте снова.")
        return
    await state.update_data(git_rep=message.text)
    data = await state.get_data()
    name = data.get("name")
    group = data.get("group")
    hw_num = data.get("hw_num")
    git_rep = data.get("git_rep")
    if None in (name, group, hw_num, git_rep):
        await message.answer("Произошла ошибка. Пожалуйста, начните заново.")
        await state.clear()
        return
    database.execute_query(
        query="""
        INSERT INTO hw(
            name1, group1, hw_num, git_rep
        ) VALUES (?, ?, ?, ?)
        """,
        params=(name, int(group), int(hw_num), git_rep)
    )
    await state.clear()
    await message.answer("ДЗ отправлено", reply_markup=ReplyKeyboardRemove())
