from symtable import Class
import ssdeep
import shutil
from PIL import Image
import imagehash
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
import keyboards as kb
from bot import bot
from db import create_empty_work, create_work, get_work_id, check_hash_file, delete_work,check_image_hash, add_file, test
import os

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
    await callback.message.answer('Ви бажаєте придбати або продати роботу ?', reply_markup=kb.buy_sell_kb)

class Sell (StatesGroup):
    Faculty = State()
    Specialty = State()
    Discipline = State()
    Title_work = State()
    Task = State()
    Mark = State()
    listing_price = State()
    file1 = State()
    file2 = State()
    file3 = State()
    file4 = State()
    file5 = State()
    file6 = State()
    file7 = State()
    file8 = State()
    file9 = State()
    file10 = State()

    end = State()

async def compute_ssdeep_hash(file_path):
     return ssdeep.hash_from_file(file_path)

@router.message(F.text == "Продати")
async def sell_work1(message: Message, state: FSMContext):
    if await accept_terms(message.from_user.id):
        await state.set_state(Sell.Faculty)
        
        await message.answer("Вкажіть факультет", reply_markup=ReplyKeyboardRemove())

@router.message(Sell.Faculty)
async def sell_work2(message: Message, state: FSMContext):
    await state.update_data(Faculty=message.text)
    await state.set_state(Sell.Specialty)
    await message.answer("Вкажіть спеціальність")

@router.message(Sell.Specialty)
async def sell_work3(message: Message, state: FSMContext):
    await state.update_data(Specialty=message.text)
    await state.set_state(Sell.Discipline)
    await message.answer("Вкажіть назву роботи")

@router.message(Sell.Discipline)
async def sell_work4(message: Message, state: FSMContext):
    await state.update_data(Discipline=message.text)
    await state.set_state(Sell.Title_work)
    await message.answer("Вкажіть дисципліну")

@router.message(Sell.Title_work)
async def sell_work5(message: Message, state: FSMContext):
    await state.update_data(Title_work=message.text)
    await state.set_state(Sell.Task)
    await message.answer("Вкажіть Завдання (plain‑text)")

@router.message(Sell.Task)
async def sell_work6(message: Message, state: FSMContext):
    await state.update_data(Task=message.text)
    await state.set_state(Sell.Mark)
    await message.answer("Вкажіть оцінку")

@router.message(Sell.Mark)
async def sell_work7(message: Message, state: FSMContext):
    await state.update_data(Mark=message.text)
    await state.set_state(Sell.listing_price)
    await message.answer("Вкажіть ціну")


@router.message(Sell.listing_price)
# @router.message(F.text == "/test")
async def sell_work8(message: Message, state: FSMContext):
    await state.update_data(listing_price=message.text)
    await state.set_state(Sell.file1)
    await message.answer("Надішліть файл з роботою, першим файлом потрібно надіслати фото з оцінкою та назвою роботи")


@router.message(Sell.file1)
async def sell_work9(message: Message, state: FSMContext):
    document = message.document
    if message.photo and not(message.media_group_id):
        photo = message.photo[-1]  # Самое "большое" фото
        file_id = photo.file_id
        user_id = message.from_user.id
        create_empty_work(user_id)
        
        file = await bot.get_file(file_id)
        file_path = file.file_path
        data = await state.get_data()
        # get_work_id(user_id)

        folder_path = "user_works/" + str(user_id)+"/"+str(get_work_id(user_id)) + "/"
        os.makedirs(folder_path, exist_ok=True)
        file = folder_path+'preview.jpg'
        
        listing_price = data.get("listing_price")
        price_with_free = round(float(listing_price) * 1.1, 2)

        await bot.download_file(file_path, file)
        image = Image.open(file)
        hash = imagehash.phash(image)
        hash = str(hash)
        
        #переделать
        if check_image_hash(hash):
            print("Фото прийнято")
        
            create_work(user_id, data.get("Faculty"), data.get("Specialty"), data.get("Discipline"), data.get("Title_work"), data.get("Task"), data.get("Mark"),
                            listing_price, price_with_free)
            
            add_file(user_id, file, "image", hash)
                
            await state.set_state(Sell.file2)

            await message.answer('надішліть наступний файл')
        else:

            await state.clear()
            await message.answer("Таке фото вже існує, спробуйте знову", reply_markup=kb.buy_sell_kb)
            
            delete_work(user_id)
            
            shutil.rmtree(folder_path)
        
    else:
        await message.answer("Ви не надіслали жодного файлу або надіслали групу, потрібно відправляти по 1 файлу, спробуйте знову відправити фото")

@router.message(Sell.file2)
async def sell_work10(message: Message, state: FSMContext):
    document = message.document
    if document != None and not(message.media_group_id):
        file_id = message.document.file_id        
        user_id = message.from_user.id
        #create_empty_work(user_id)

        file = await bot.get_file(file_id)
        file_path = file.file_path
        data = await state.get_data()
        get_work_id(user_id)

        folder_path = "user_works/" + str(user_id)+"/"+str(get_work_id(user_id)) + "/"
        os.makedirs(folder_path, exist_ok=True)
        file = folder_path+document.file_name
        
        #listing_price = data.get("listing_price")
        #price_with_fee = round(float(listing_price) * 1.1, 2)
        
        await bot.download_file(file_path, file)
        hash = await compute_ssdeep_hash(file)

        if check_hash_file(hash):
            print("Файл прийнято")
        
            #create_work(user_id, data.get("Faculty"), data.get("Specialty"), data.get("Discipline"), data.get("Title_work"), data.get("Task"), data.get("Mark"),listing_price, price_with_fee, file1, hash )
            
            add_file(user_id, file, "document", hash)

            # await state.set_state(Sell.file3)

            await message.answer('надішліть наступний файл або натисніть кнопку завершити', reply_markup=kb.files_end_kb)

        else:
            await state.clear()
            await message.answer("Така робота вже існує, спробуйте знову", reply_markup=kb.buy_sell_kb)
            
            delete_work(user_id)
            
            shutil.rmtree(folder_path)

    else:
        if message.text != "Завершити":
            await message.answer("Ви не надіслали жодного файлу або надіслали групу, потрібно відправляти по 1 файлу, спробуйте знову")

# @router.message(F.text == "/test")
# async def test1(message: Message, state: FSMContext):
#     print(getattr(test(),'file2'))


@router.message(StateFilter(Sell.end, Sell.file2, Sell.file3, Sell.file4, Sell.file5,
                            Sell.file6, Sell.file7, Sell.file8, Sell.file9, Sell.file10),
                F.text == "Завершити")
async def sell_work(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Ваша робота виставлена на продаж, перевірте вкладку мої роботи', reply_markup=kb.buy_sell_kb)





