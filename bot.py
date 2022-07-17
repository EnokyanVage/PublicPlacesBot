from secrets import choice
from telebot import types
from array import *
import time
import emoji

from data import config
from database import user_base, category_base, placescategory, places_photo, places_base

from user_functionality import registration, user_del, changeacc

from publicplaces_functionality import newplaces, allpp, PublicPleace_del, searchpp

from auxiliary_files import validation


key_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_stop.add(types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))


last_time = {}

time_ddos = int(1500)


def antiddos(message): 
    if message.chat.id not in last_time: 
        last_time[message.chat.id] = []
        last_time[message.chat.id].append(time.time())
        last_time[message.chat.id].append(0)
    else:
        if last_time[message.chat.id][1] < int(5):

            if (time.time() - last_time[message.chat.id][0]) * 1000 < time_ddos:
                config.bot.send_message(message.from_user.id, "Не спамь! А то получишь бан.")
                last_time[message.chat.id][1] += 1
                if last_time[message.chat.id][1] == 5:
                    config.bot.send_message(message.from_user.id, "Вы забанены на 5 минут.")
                return True
            
            last_time[message.chat.id][0] = time.time()
        else:
            if (time.time() - last_time[message.chat.id][0]) * 1000 >= 300000:
                last_time[message.chat.id][1] = 0
            return True
        
    return False

@config.bot.message_handler(commands=['start'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False) or user_base.users_dictionary.get(message.from_user.id) != None:
            config.bot.send_message(message.from_user.id, "Мы уже стартанули ;)")
        else:
            config.bot.send_message(message.from_user.id, config.HELLO_REG)


@config.bot.message_handler(commands=['help'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False) or user_base.users_dictionary.get(message.from_user.id) != None:
            config.bot.send_message(message.from_user.id, config.HELP)
        else:
            config.bot.send_message(message.from_user.id, config.HELP_NEW_USER)


@config.bot.message_handler(commands=['info'])
def start_message(message):

    if antiddos(message) == False:
        config.bot.send_message(message.from_user.id, config.INFO)

@config.bot.message_handler(commands=['web'])
def start_message(message):

    if antiddos(message) == False:
        config.bot.send_message(message.from_user.id, config.WEB)

@config.bot.message_handler(commands=['reg'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False) or user_base.users_dictionary.get(message.from_user.id) != None:
            config.bot.send_message(message.from_user.id, "Этап регистрации уже пройден " + emoji.emojize(':grinning_face:'))
        else:
            user_base.users_dictionary[message.from_user.id] = []
            config.bot.send_message(message.from_user.id, "Регистрация!",reply_markup=key_stop)
            config.bot.send_message(message.from_user.id, "Ваше имя?")
            config.bot.register_next_step_handler(message, registration.get_name)


@config.bot.message_handler(commands=['del'])
def start_message(message):

    print(str(message.from_user.id) + " " + str(user_base.check_user(message.from_user.id)))
    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Да" + emoji.emojize(':check_mark_button:')), types.KeyboardButton("Нет" + emoji.emojize(':prohibited:')))
            config.bot.send_message(message.from_user.id, "Вы уверены, что хотите удалить данные регистрации?\n\nВместе с данными регистрации удалятся размещенные общественные места.", reply_markup=rmk)

            if user_base.users_dictionary.get(message.from_user.id) != None:
                user_base.users_dictionary.pop(message.from_user.id)

            config.bot.register_next_step_handler(message,user_del.del_user)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")

@config.bot.message_handler(commands=['newpp'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, config.NEWPP)
            config.bot.send_message(message.from_user.id, "Введите название компании:",reply_markup=key_stop)
            config.bot.register_next_step_handler(message,newplaces.get_type)
            places_base.pps_dictionary[message.from_user.id] = []
            placescategory.pc_dictionary[message.from_user.id] = []
            places_photo.photo_dictionary[message.from_user.id] = []
        else: 
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")


@config.bot.message_handler(commands=['allpp'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, "Список доступных PublicPlaces в вашем городе:")
            cw = places_base.count_places()
                
            if cw > 0:
                allpp.send_character_page(message)
            else:
                config.bot.send_message(message.from_user.id, "К сожаления в вашем городе нет доступных PublicPlaces" + emoji.emojize(':pensive_face:'))
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")

@config.bot.message_handler(commands=['getpp'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, "Отправьте номер PublicPlace.",reply_markup = key_stop)
            config.bot.register_next_step_handler(message, allpp.get_pp)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")

@config.bot.message_handler(commands=['delpp'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id,places_base.get_mypp_pages(message.from_user.id))
            config.bot.send_message(message.from_user.id, "Удаление PublicPlace:\n\nВведите номер PublicPlace в базе, которую хотите удалить.",reply_markup=key_stop)
            config.bot.register_next_step_handler(message, PublicPleace_del.del_places)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")


@config.bot.message_handler(commands=['searchpp'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, config.SEARCHPP)
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Поесть" + emoji.emojize(':fork_and_knife_with_plate:')), 
                    types.KeyboardButton("Красота" + emoji.emojize(':lipstick:')), 
                    types.KeyboardButton("Цветы" + emoji.emojize(':bouquet:')), 
                    types.KeyboardButton("Медицина" + emoji.emojize(':lab_coat:')), 
                    types.KeyboardButton("Развлечение" + emoji.emojize(':confetti_ball:')), 
                    types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))

            config.bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=rmk)
            searchpp.search_dictionary[message.from_user.id] = []
            places_base.get_pages_cat[message.from_user.id] = []
            config.bot.register_next_step_handler(message, searchpp.get_category)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")



@config.bot.message_handler(commands=['mypp'])
def start_message(message):
    
    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            myw = places_base.get_mypp_c(message.from_user.id)
            
            if myw > 0:
                config.bot.send_message(message.from_user.id, "Список ваших PublocPlace:")
                config.bot.send_message(message.from_user.id, places_base.get_mypp_pages(message.from_user.id) + "Если хотите удалить какую-то общественное место, воспользуйтесь командой /delpp")
            else:
                config.bot.send_message(message.from_user.id, "Размещенные вами в PublocPlace не найдены.\n\nДля размещения общественного места, воспользуйтесь командой /newpp")
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")



@config.bot.message_handler(commands=['infoempl'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, config.EMPLOYER)
        else: 
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")


@config.bot.message_handler(commands=['infopp'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, config.SEEKER)
        else: 
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")


@config.bot.message_handler(commands=['myinfo'])
def start_message(message):
    mes = message.text
    if antiddos(message) == False:
    
        config.bot.send_message(message.from_user.id,"Информация о вашем аккаунте:\n")
        inf = user_base.get_myinfo(message.from_user.id)

        s_mess = inf
        if inf == None:
            s_mess = "Не найдена."
        else:
            s_mess += 'У вас ' + validation.pps(places_base.get_mypp_c(message.from_user.id)) + '\n\n'
            s_mess += 'Для просмотра своих активных PublocPlace воспользуйтесь командой /mypp'
        config.bot.send_message(message.from_user.id,s_mess)


@config.bot.message_handler(commands=['name'])
def start_message(message):
    
    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, "Изменение имени.\n\nВведите имя:",reply_markup = key_stop)
            config.bot.register_next_step_handler(message, changeacc.name)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")
    


@config.bot.message_handler(commands=['surname'])
def start_message(message):

    if antiddos(message) == False:
        if (user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, "Изменение фамилии.\n\nВведите Фамилию:",reply_markup = key_stop)
            config.bot.register_next_step_handler(message, changeacc.surname)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")
    


@config.bot.message_handler(commands=['age'])
def start_message(message):
    
    if antiddos(message) == False:
        if( user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, "Изменение возраста.\n\nВведите возраст:",reply_markup = key_stop)
            config.bot.register_next_step_handler(message, changeacc.age)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")


@config.bot.message_handler(commands=['city'])
def start_message(message):

    if antiddos(message) == False:
        if( user_base.check_user(message.from_user.id) != False):
            config.bot.send_message(message.from_user.id, "Изменение города.\n\nВведите город:",reply_markup = key_stop)
            config.bot.register_next_step_handler(message, changeacc.city)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")
    

@config.bot.message_handler(commands=['gender'])
def start_message(message):

    if antiddos(message) == False:
        if( user_base.check_user(message.from_user.id) != False):
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton("Мужской" + emoji.emojize(':man:')), types.KeyboardButton("Женский" + emoji.emojize(':woman:')), types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))


            config.bot.send_message(message.from_user.id, "Изменение пола.",reply_markup = rmk)
            config.bot.register_next_step_handler(message, changeacc.gender)
        else:
            config.bot.send_message(message.from_user.id, "Сначала зарегистрируйтесь! " + emoji.emojize(':grinning_face:') + " /reg")



@config.bot.message_handler(content_types=['text'])
def handler_text_message(message):
    mes = message.text

    if antiddos(message) == False:
        config.bot.send_message(message.from_user.id, config.ERROR)
    
  
          
if __name__ == '__main__':
    user_base.init_db(True)
    places_base.init_db(True)
    category_base.init_db(True)
    insert_into = [(1,'Поесть'),(2,'Красота'),(3,'Цветы'),(4,'Медицина'),(5,'Развлечения')]
    category_base.add_category()
    places_photo.init_db(True)
    placescategory.init_db(True)


    config.bot.polling(none_stop=True, interval=0)
