from symtable import Class

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboards as kb
from bot import bot



from db import create_user, accept_terms, accepted_terms

router =Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    if not(await accept_terms(message.from_user.id)):
        await message.answer("условия и правила", reply_markup=kb.accept)
    else:
        await message.answer('Ви бажаєте придбати або продати роботу ?',reply_markup= kb.buy_sell_kb)

@router.callback_query(F.data == "accept_terms")
async def accepted(callback: CallbackQuery):
    await accepted_terms(callback.from_user.id)
    await callback.message.delete()

class Sell (StatesGroup):
    Faculty = State()
    Specialty = State()
    Discipline = State()
    Title_work = State()
    Task = State()
    grade = State()
    Price = State()
    file1 = State()
    file2 = State()
    file3 = State()
    file4 = State()
    file5 = State()

@router.message(F.text == "Продати")
async def sell_work1(message: Message, state: FSMContext):
    if await accept_terms(message.from_user.id):
        await state.set_state(Sell.Faculty)
        await message.answer("Вкажіть факультет")

@router.message(Sell.Faculty)
async def sell_work2(message: Message, state: FSMContext):
    await state.update_data(Faculty=message.text)
    await state.set_state(Sell.Specialty)
    await message.answer("Вкажіть спеціальність")

@router.message(Sell.Specialty)
async def sell_work3(message: Message, state: FSMContext):
    await state.update_data(Specialty=message.text)
    await state.set_state(Sell.Title_work)
    await message.answer("Вкажіть назву роботи")

@router.message(Sell.Title_work)
async def sell_work4(message: Message, state: FSMContext):
    await state.update_data(Title_work=message.text)
    await state.set_state(Sell.Task)
    await message.answer("Вкажіть Завдання (plain‑text)")

@router.message(Sell.Task)
async def sell_work5(message: Message, state: FSMContext):
    await state.update_data(Task=message.text)
    await state.set_state(Sell.Price)
    await message.answer("Вкажіть ціну")

@router.message(Sell.Price)
async def sell_work6(message: Message, state: FSMContext):
    await state.update_data(Price=message.text)
    await state.set_state(Sell.file1)
    await message.answer("Надішліть файл з роботою")

@router.message(Sell.file1)
async def sell_work7(message: Message, state: FSMContext):
    document = message.document
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    print(file_path)
    print(type(file_path))
    await bot.download_file(file_path, document.file_name)







