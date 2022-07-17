from telebot import types
import emoji

from data import config
from database import user_base
from auxiliary_files import validation

del_keyb = types.ReplyKeyboardRemove()
dictionary_gender = {'Мужской' + emoji.emojize(':man:'): 'Мужской', 'Женский' + emoji.emojize(':woman:'): 'Женский'}
def name(message):

    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        change_stop(message)
    elif validation.validateName(message.text):
        user_base.update_name(message.text,message.from_user.id)
        config.bot.send_message(message.from_user.id, "Имя изменено.",reply_markup=del_keyb)
    else:
        config.bot.send_message(message.from_user.id, "Имя введено не корректно! Повторите попытку.")
        config.bot.register_next_step_handler(message,name)
        

def surname(message):

    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        change_stop(message)
    elif validation.validateName(message.text):
        user_base.update_surname(message.text,message.from_user.id)
        config.bot.send_message(message.from_user.id, "Фамилия изменена.",reply_markup=del_keyb)
    else:
        config.bot.send_message(message.from_user.id, "Фамилия введена не корректно! Повторите попытку.")
        config.bot.register_next_step_handler(message,surname)

def age(message):

    flag_age = True
    age_i = 0
    
    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        change_stop(message)
        return
    
    try:
        age_i = int(message.text)
    except Exception:
        flag_age = False
        config.bot.send_message(message.from_user.id, "Цифрами, пожалуйста")
        age_i = int(0)
        
    if age_i > 0 and flag_age == True:
        user_base.update_age(age_i,message.from_user.id)
        config.bot.send_message(message.from_user.id, "Возраст изменён.",reply_markup=del_keyb)
    else:
        config.bot.send_message(message.from_user.id, "Возраст введен не корректно!\nПовторите попытку.")
        config.bot.register_next_step_handler(message, age)

def gender(message):
    
    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        change_stop(message)
    elif message.text in dictionary_gender.keys():
        user_base.update_gender(str(message.text),message.from_user.id)
        config.bot.send_message(message.from_user.id, "Пол изменён.",reply_markup=del_keyb)
    else:
        config.bot.send_message(message.from_user.id, "Пол введено не корректно! Повторите попытку.")
        config.bot.register_next_step_handler(message,gender)

def city(message):

    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        change_stop(message)
    elif message.text == 'Новосибирск':
        user_base.update_city(message.text,message.from_user.id)
        config.bot.send_message(message.from_user.id, "Город изменён.",reply_markup=del_keyb)
    else:
        config.bot.send_message(message.from_user.id, "Я не знаю такого города! Повторите попытку.")
        config.bot.register_next_step_handler(message,city)


def change_stop(message):
    config.bot.send_message(message.from_user.id, "Остановил.",reply_markup=del_keyb)