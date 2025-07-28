from aiogram.types import (CallbackQuery, KeyboardButton, ReplyKeyboardMarkup,
                           inline_keyboard_markup, InlineKeyboardButton, InlineKeyboardMarkup)

accept = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ok', callback_data = "accept_terms")]
    ])

buy_sell_kb = ReplyKeyboardMarkup( keyboard=[
    [KeyboardButton(text="Придбати")],[KeyboardButton(text="Продати")]],
    resize_keyboard=True, one_time_keyboard=True)

files_end_kb = ReplyKeyboardMarkup( keyboard=[
    [KeyboardButton(text="Завершити")]],
    resize_keyboard=True, one_time_keyboard=True)