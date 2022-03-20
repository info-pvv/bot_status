from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.handlers.common import cmd_start,admin_list
from app.handlers.db import get_health,insert_health,update_health,get_disease,insert_disease,update_disease,get_list

available_health = ["здоров", "болен","отпуск","учеба","удаленка"]
available_health1 = ["болен"]
available_disease = ["орви", "ковид", "давление", "понос", "прочее"]


class OrderHealth(StatesGroup):
    waiting_for_health = State()
    waiting_for_disease = State()
    

async def health_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_health:
        keyboard.add(name)
    await message.answer(f"{message.from_user.first_name} {message.from_user.last_name},выберите статус:", allow_sending_without_reply=True, reply_markup=keyboard)
    await OrderHealth.waiting_for_health.set()
   

async def health_chosen(message: types.Message, state: FSMContext):
    print(f"heath_chosen {message.text.lower()}")
    if message.text.lower() not in available_health1:
        await state.update_data(chosen_health=message.text.lower())
        health_userid = get_health(message.from_user.id)
        print(health_userid)
        if (health_userid == None):
            insert_health(message.from_user.id,message.text)
        else:
            update_health(message.from_user.id,message.text)
        disease_userid = get_disease(message.from_user.id)
        print(disease_userid)
        if (disease_userid == None):
            insert_disease(message.from_user.id,"")
        else:
            update_disease(message.from_user.id,"")
        user_data = await state.get_data()
        await message.answer(f"{message.from_user.first_name} {message.from_user.last_name}. Статус: {user_data['chosen_health']}.", reply_markup=types.ReplyKeyboardRemove())
        print(f"health_chosen cmd_start")
        await state.finish()
        return
    await state.update_data(chosen_health=message.text.lower())
    health_userid = get_health(message.from_user.id)
    print(health_userid)
    if (health_userid == None):
        insert_health(message.from_user.id,message.text)
    else:
        update_health(message.from_user.id,message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_disease:
        keyboard.add(size)
    await OrderHealth.next()
    await message.answer("Теперь выберите заболевание:", reply_markup=keyboard)
    #await message.answer(f"Вы заболели {message.text.lower()} {user_data['chosen_healt']}.", reply_markup=types.ReplyKeyboardRemove())
    #await state.finish()

async def disease_chosen(message: types.Message, state: FSMContext):
    print(f"disease_chosen {message.text.lower()}")
    if message.text.lower() not in available_disease:
        await message.answer("Пожалуйста, заболевание, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_disease=message.text.lower())
    user_data = await state.get_data()
    disease_userid = get_disease(message.from_user.id)
    print(disease_userid)
    if (disease_userid == None):
        insert_disease(message.from_user.id,message.text)
    else:
        update_disease(message.from_user.id,message.text)
    await message.answer(f"{message.from_user.first_name} {message.from_user.last_name}. Статус: {user_data['chosen_health']}. Заболевание: {user_data['chosen_disease']}", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    print(f"disease_chosen cmd_start")
    #await OrderHealth.waiting_for_start.set()

async def health_list_all(message: types.Message, state: FSMContext):
    get_list_all=get_list()
    string_to_send = ''
    hop_count = 0
    ill_count = 0
    for tuple in get_list_all:
        for string_to_append in tuple:
            string_to_send += str(string_to_append)+' '
        string_to_send += '\n' 
        hop_count +=1
        if (tuple[2]=="болен"):
            ill_count+=1
            
    await message.answer(f'Количество работников - {hop_count}, больных - {ill_count}') 
    await message.answer(string_to_send, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

def register_handlers_health(dp: Dispatcher):
    dp.register_message_handler(health_start, commands="health", state="*")
    dp.register_message_handler(health_start,lambda msg: msg.text == "Здоровье", state="*")
    dp.register_message_handler(health_list_all,lambda msg: msg.text == "Отчет по сотрудникам", state="*")
    dp.register_message_handler(admin_list,lambda msg: msg.text == "Админка", state="*")
    dp.register_message_handler(health_chosen, state=OrderHealth.waiting_for_health)
    dp.register_message_handler(disease_chosen, state=OrderHealth.waiting_for_disease)
    

