from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from app.handlers.db import get_list_all
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


async def remove_report(message: types.Message, state: FSMContext):
    get_list=get_list_all()
    string_to_send = ''
    hop_count = 0
    inline_kb_full=InlineKeyboardMarkup(row_width=3)
    #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = []
    for tuple in get_list:
        inline_btn = InlineKeyboardButton('str(tuple[0])', callback_data='str(tuple[0])')
        inline_kb_full.add(inline_btn)
        #buttons.append(str(tuple[0]))
        for string_to_append in tuple:
            string_to_send += str(string_to_append)+' '
        string_to_send += '\n' 
        hop_count +=1
    #buttons.append("Выйти")
    inline_btn = InlineKeyboardButton("Выйти", callback_data="Выйти")
    inline_kb_full.add(inline_btn)
    print(buttons)
    #keyboard.add(*buttons)
    await message.answer(f'Количество записей работников в базе - {hop_count}')
    await message.answer(f'Выберите номер, кого следует исключить из отчета')
    await message.answer(string_to_send, reply_markup=inline_kb_full)
    
    

def register_handlers_admin(dp: Dispatcher):
        dp.register_message_handler(remove_report, Text(equals="Исключить из отчета", ignore_case=True), state="*")
        dp.register_message_handler(remove_report, Text(equals="Включить в отчет", ignore_case=True), state="*")
        dp.register_message_handler(remove_report, Text(equals="Дать админ. права", ignore_case=True), state="*")
        dp.register_message_handler(remove_report, Text(equals="Забрать админ права", ignore_case=True), state="*")


