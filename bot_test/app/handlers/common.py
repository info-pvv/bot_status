from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from app.handlers.db import get_users,insert_users,update_users,insert_FIO,get_user_status_admin,insert_id_status

available_choise = {"Здоровье":1,"Админка":0,"Отчет по сотрудникам":0}
available_admin = {"Исключить из отчета":0,"Включить в отчет":0,"Дать админ. права":0,"Забрать админ права":0,"Выйти":0}
def create_keyboard(user_id,menu):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for choise in menu.keys():
        if (menu[choise]==1):
            keyboard.add(choise)
        else:
            if (get_user_status_admin(user_id)):
                keyboard.add(choise)
    return keyboard
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_1 = get_users(message.from_user.id)
    print(user_1)
    if (user_1 == None):
        insert_users(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username)
        insert_FIO(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username)
        insert_id_status(message.from_user.id,False,False)
    else:
        update_users(message.from_user.id,message.from_user.first_name,message.from_user.last_name,message.from_user.username)
    keyboard = create_keyboard(message.from_user.id,available_choise)
    await message.answer("Выберите, что хотите отметить:", reply_markup=keyboard)
   

async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())

async def admin_list(message: types.Message, state: FSMContext):
    keyboard = create_keyboard(message.from_user.id,available_admin)
    await message.answer("Выберите, действие:", reply_markup=keyboard)
    
def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_start, Text(equals="Выйти", ignore_case=True), state="*")
    
