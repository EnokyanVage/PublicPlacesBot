from telebot import types
import emoji

from data import config
from auxiliary_files import validation
from database import user_base

key_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_stop.add(types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))

dictionary_gender = {'Мужской' + emoji.emojize(':man:'): 'Мужской', 'Женский' + emoji.emojize(':woman:'): 'Женский'}
def get_name(message):
    name = message.text.title()

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_reg(message.from_user.id)
    elif validation.validateName(name):
        user_base.users_dictionary[message.from_user.id].append(name)
        config.bot.send_message(message.from_user.id, "Ваша фамилия?")
        config.bot.register_next_step_handler(message,get_surname)
    else:
        config.bot.send_message(message.from_user.id, "Имя введено не корректно! Повторите попытку.")
        config.bot.register_next_step_handler(message,get_name)


def get_surname(message): 
    surname = message.text.title()

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_reg(message.from_user.id)
    elif validation.validateName(surname):
        user_base.users_dictionary[message.from_user.id].append(surname)
        config.bot.send_message(message.from_user.id, "Ваш возраст?")
        config.bot.register_next_step_handler(message, get_age)
    else:
        config.bot.send_message(message.from_user.id, "Фамилия введена не корректно! Повторите попытку.")
        config.bot.register_next_step_handler(message, get_surname)
        

def get_age(message):
    flag_age = True
    age = 0

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_reg(message.from_user.id)
        return

    try:
        age = int(message.text) #проверяем, что возраст введен корректно
    except Exception:
        flag_age = False
        config.bot.send_message(message.from_user.id, "Цифрами, пожалуйста")
        age = int(0)
        
    if age > 12 and flag_age == True:
        user_base.users_dictionary[message.from_user.id].append(age)
        
        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rmk.add(types.KeyboardButton("Мужской" + emoji.emojize(':man:')), types.KeyboardButton("Женский" + emoji.emojize(':woman:')), types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))

        config.bot.send_message(message.from_user.id, "Ваш пол?", reply_markup=rmk)

        config.bot.register_next_step_handler(message, get_gender)
    else:
        config.bot.send_message(message.from_user.id, "Возраст введен не корректно!\nПовторите попытку.\nПредупреждение: Допустимый возраст от 12 лет.")
        config.bot.register_next_step_handler(message, get_age)
        
    
def get_gender(message):
    
    g = message.text
    
    gender = ' '

    if g == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_reg(message.from_user.id)
        return
    print(g)
    if g in dictionary_gender.keys():
        user_base.users_dictionary[message.from_user.id].append(str(dictionary_gender[g]))
        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, "Ваш город?", reply_markup=key_stop)
        config.bot.register_next_step_handler(message, get_city,)
    elif g != ' ':
        config.bot.send_message(message.from_user.id,"Введите Мужской или Женский!")
        config.bot.register_next_step_handler(message, get_gender) 
        


def get_city(message):
    city = message.text
    city = city.title()

    if city == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_reg(message.from_user.id)
        return

    if validation.check_city(city):
        user_base.users_dictionary[message.from_user.id].append(city)
        
        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, "Проверьте введенные данные:",reply_markup=del_keyb)
        
        result = get_data_dict(message.from_user.id)
        result += "Если данные верны, нажмите кнопку сохранить!\nИначе отменить."

        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Сохранить', callback_data='save')
        keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='Отменить', callback_data='cancel')
        keyboard.add(key_no)

        config.bot.send_message(message.from_user.id, text=result, reply_markup=keyboard)
    else:
        config.bot.send_message(message.from_user.id,"Я не знаю такого города! Повторите попытку.")
        config.bot.register_next_step_handler(message, get_city)



@config.bot.callback_query_handler(func=lambda call: call.data.startswith('save')) 
def callback_worker_save(call):

    try:
        result = get_data_dict(call.from_user.id)
        if( user_base.check_user(call.from_user.id) == False):
            user_id = call.from_user.id
            name = user_base.users_dictionary[call.from_user.id][0]
            surname = user_base.users_dictionary[call.from_user.id][1] 
            age = user_base.users_dictionary[call.from_user.id][2]
            gender = user_base.users_dictionary[call.from_user.id][3]
            city = user_base.users_dictionary[call.from_user.id][4]

            val = (user_id, name, surname, age, gender, city)

            user_base.add_user(val)
            user_base.users_dictionary.pop(call.from_user.id)
            config.bot.send_message(call.message.chat.id, "Данные сохранены!\nРегистрация пройдена.\n\nДля просмотра доступных вам функций воспользуйтесь /help")
        else:
            config.bot.send_message(call.message.chat.id, "Вы уже сохранили данные!")
        config.bot.edit_message_text(result, chat_id=call.from_user.id, message_id=call.message.id)
    except:
        config.bot.delete_message(call.message.chat.id, call.message.message_id)
        config.bot.send_message(call.message.chat.id, "Извините, произошел сбой. Повторите попытку")
    

     
@config.bot.callback_query_handler(func=lambda call: call.data.startswith('cancel')) 
def callback_worker_cancel(call):

    result = get_data_dict(call.from_user.id)
    if( user_base.check_user(call.from_user.id) == False):
        user_base.users_dictionary.pop(call.from_user.id)
        config.bot.send_message(call.message.chat.id, "Данные не сохранены!\nРегистрация не пройдена.\nПовторить попытку /reg")
    else:
        config.bot.send_message(call.message.chat.id, "Этот шаг уже пройден!")
    config.bot.edit_message_text(result, chat_id=call.from_user.id, message_id=call.message.id)
        
         
def stop_reg(user_id: int):
    del_keyb = types.ReplyKeyboardRemove()
    if( user_base.check_user(user_id) == False):
        user_base.users_dictionary.pop(user_id)
        config.bot.send_message(user_id, "Данные не сохранены!\nРегистрация не пройдена.\nПовторить попытку /reg",reply_markup=del_keyb)
    


def get_data_dict(id_u: int):
    result = "Вы: " + user_base.users_dictionary[id_u][0] + " " + user_base.users_dictionary[id_u][1] + "\n"
    result += "Вам: " + validation.years(user_base.users_dictionary[id_u][2]) + "\n"
    result += "Пол: " + user_base.users_dictionary[id_u][3] + "\n"
    result += "Ваш город: " + user_base.users_dictionary[id_u][4] + "\n"
    return result