from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.handlers.db import get_list_all,get_user_id,update_report,update_admin
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

code_list=[]

class OrderAdmin(StatesGroup):
    waiting_for_remove_report = State()
    waiting_for_enable_report = State()
    waiting_for_remove_admin = State()
    waiting_for_enable_admin = State()

async def admin_action(message: types.Message, state: FSMContext):
    get_list=get_list_all()
    string_to_send = ''
    code_list=[]
    hop_count = 0
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for tuple in get_list:
        code_list.append(str(tuple[0]))
        buttons.append(str(tuple[0]))
        for string_to_append in tuple:
            string_to_send += str(string_to_append)+' | '
        string_to_send += '\n' 
        hop_count +=1
    print(code_list)
    keyboard.add(*buttons)
    await message.answer(f'Количество записей работников в базе - {hop_count}')
    await message.answer(f'Выберите номер, кого следует исключить из отчета')
    await message.answer(string_to_send, reply_markup=keyboard)
    if (message.text=="Исключить из отчета"):
        await OrderAdmin.waiting_for_remove_report.set()
    elif (message.text=="Включить в отчет"):
        await OrderAdmin.waiting_for_enable_report.set()
    elif (message.text=="Дать админ. права"):
        await OrderAdmin.waiting_for_enable_admin.set()
    elif (message.text=="Забрать админ права"):
        await OrderAdmin.waiting_for_remove_admin.set()

async def remove_report_kb(message: types.Message, state: FSMContext):
    print(f'Нажата кнопка {message.text}')
    await message.answer(f"{message.text} исключен из отчета", reply_markup=types.ReplyKeyboardRemove())
    user_id=get_user_id(message.text)
    update_report(user_id,False)
    await state.finish()
    return
async def enable_report_kb(message: types.Message, state: FSMContext):
    print(f'Нажата кнопка {message.text}')
    await message.answer(f"{message.text} включен в отчет", reply_markup=types.ReplyKeyboardRemove())
    user_id=get_user_id(message.text)
    update_report(user_id,True)
    await state.finish()
    return
async def enable_admin_kb(message: types.Message, state: FSMContext):
    print(f'Нажата кнопка {message.text}')
    await message.answer(f"{message.text} выданы админ права", reply_markup=types.ReplyKeyboardRemove())
    user_id=get_user_id(message.text)
    update_admin(user_id,True)
    await state.finish()
    return
async def remove_admin_kb(message: types.Message, state: FSMContext):
    print(f'Нажата кнопка {message.text}')
    await message.answer(f"{message.text} изъяты админ права", reply_markup=types.ReplyKeyboardRemove())
    user_id=get_user_id(message.text)
    update_admin(user_id,False)
    await state.finish()
    return

    

def register_handlers_admin(dp: Dispatcher):
        dp.register_message_handler(admin_action, Text(equals="Исключить из отчета", ignore_case=True), state="*")
        dp.register_message_handler(admin_action, Text(equals="Включить в отчет", ignore_case=True), state="*")
        dp.register_message_handler(admin_action, Text(equals="Дать админ. права", ignore_case=True), state="*")
        dp.register_message_handler(admin_action, Text(equals="Забрать админ права", ignore_case=True), state="*")
        dp.register_message_handler(remove_report_kb, state=OrderAdmin.waiting_for_remove_report)
        dp.register_message_handler(enable_report_kb, state=OrderAdmin.waiting_for_enable_report)
        dp.register_message_handler(remove_admin_kb, state=OrderAdmin.waiting_for_remove_admin)
        dp.register_message_handler(enable_admin_kb, state=OrderAdmin.waiting_for_enable_admin)
        
        


