from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
import keyboards as kb

from db import create_user, accept_terms, accepted_terms

router =Router()

@router.message(CommandStart())
async def start(message: Message):
    await create_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    if not(await accept_terms(message.from_user.id)):
        await message.answer("условия и правила", reply_markup=kb.accept)
    else:
        await message.answer('',reply_markup= kb.buy_sell_kb)

@router.callback_query(F.data == "accept_terms")
async def accepted(callback: CallbackQuery):
    await accepted_terms(callback.from_user.id)
    await callback.message.delete()

@router.message(F.text == "Продати роботу")
async def sell_work(message: Message):
    if await accept_terms(message.from_user.id):
        await message.answer("Продати роботу")
