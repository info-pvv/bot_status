from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.handlers.db import get_list_all
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

code_list=[]

class OrderAdmin(StatesGroup):
    waiting_for_remove_report = State()
    waiting_for_enable_report = State()

async def remove_report(message: types.Message, state: FSMContext):
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
            string_to_send += str(string_to_append)+' '
        string_to_send += '\n' 
        hop_count +=1
    print(code_list)
    keyboard.add(*buttons)
    await message.answer(f'Количество записей работников в базе - {hop_count}')
    await message.answer(f'Выберите номер, кого следует исключить из отчета')
    await message.answer(string_to_send, reply_markup=keyboard)
    await OrderAdmin.waiting_for_remove_report.set()

async def remove_report_kb(message: types.Message, state: FSMContext):
    print(f'Нажата кнопка из {message.text}')
    await message.answer(f"{message.text}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    return
    

def register_handlers_admin(dp: Dispatcher):
        dp.register_message_handler(remove_report, Text(equals="Исключить из отчета", ignore_case=True), state="*")
        dp.register_message_handler(remove_report, Text(equals="Включить в отчет", ignore_case=True), state="*")
        dp.register_message_handler(remove_report, Text(equals="Дать админ. права", ignore_case=True), state="*")
        dp.register_message_handler(remove_report, Text(equals="Забрать админ права", ignore_case=True), state="*")
        dp.register_message_handler(remove_report_kb, state=OrderAdmin.waiting_for_remove_report)
        


