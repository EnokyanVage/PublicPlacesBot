from telebot import types
from geopy.geocoders import Nominatim
from pathlib import Path
import emoji

from data import config
from auxiliary_files import validation
from auxiliary_files import location
from database import places_base
from database import placescategory
from database import places_photo

rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
rmk.add(types.KeyboardButton("Договорная"))
rmk.add(types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))

key_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_stop.add(types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))

# list_category = {'Поесть': 1, 'Красота': 2, 'Цветы': 3, 'Медицина': 4, 'Развлечение': 5}
list_category = {'Поесть' + emoji.emojize(':fork_and_knife_with_plate:'): 1, 'Красота' + emoji.emojize(':lipstick:'): 2, 'Цветы' + emoji.emojize(':bouquet:'): 3, 'Медицина' + emoji.emojize(':lab_coat:'): 4, 'Развлечение' + emoji.emojize(':confetti_ball:'): 5}

def get_type(message):
    
    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        stop_newpp(message.from_user.id)
    elif validation.validationText(message.text):
        
        places_base.pps_dictionary[message.from_user.id].append(message.text)
        config.bot.send_message(message.from_user.id, "Укажите номер телефона.")
        config.bot.register_next_step_handler(message,get_contact)
    else:
        config.bot.send_message(message.from_user.id, "Не коректный ввод! Повторите попытку.")
        config.bot.register_next_step_handler(message,get_type)

def check_coords(coords:str):
    
    if validation.validationGeo(coords) == False:
        geolocator = Nominatim(user_agent="my_request")
        location = geolocator.geocode(coords)
        try:
            coords = str(location.longitude) +","+ str(location.latitude)
        except Exception:
            coords = " "

        print("Else: " + coords)
    return coords

def get_contact(message):

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_newpp(message.from_user.id)
        return

    if validation.validatePhone(message.text):
        places_base.pps_dictionary[message.from_user.id].append(message.text)
        config.bot.send_message(message.from_user.id, config.LOCATION,reply_markup = key_stop)
        config.bot.register_next_step_handler(message, get_location)
    else:
        config.bot.send_message(message.from_user.id, "Введите номер, например:\n+79999999999\n89999999999")
        config.bot.register_next_step_handler(message,get_contact)

def get_location(message):

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_newpp(message.from_user.id)
        return

    coords = ""
    
    print("Геолокация от ")
    print(message.from_user.id)
    print(str(message.text) + "\n\n\n")

    if message.text == None:
        current_position = (message.location.longitude, message.location.latitude)
        #создаем строку в виде ДОЛГОТА,ШИРИНА
        coords = f"{current_position[0]},{current_position[1]}"
    else:
        coords = check_coords(message.text)
        
    street = location.get_address_from_coords(coords)
   
    if street == False:
        config.bot.send_message(message.from_user.id, config.ERROR_LOCATION)
        config.bot.send_message(message.from_user.id, config.LOCATION)
        config.bot.register_next_step_handler(message, get_location)
    else:
        places_base.pps_dictionary[message.from_user.id].append(coords)
        config.bot.send_message(message.from_user.id, "Опишите общественное место")
        config.bot.register_next_step_handler(message, get_about)

def get_about(message):
  
    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_newpp(message.from_user.id)
    elif validation.validationText(message.text):
        places_base.pps_dictionary[message.from_user.id].append(message.text)
        config.bot.send_message(message.from_user.id, "Укажите время работы")
        config.bot.register_next_step_handler(message, get_time_work)
    else:
        config.bot.send_message(message.from_user.id, "Не коректный ввод! Повторите попытку.")
        config.bot.register_next_step_handler(message,get_about)      

def get_time_work(message):
    
    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        stop_newpp(message.from_user.id)
    elif validation.validationText(message.text):
        places_base.pps_dictionary[message.from_user.id].append(message.text)

        rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # rmk.add(types.KeyboardButton("Поесть"), types.KeyboardButton("Красота"), types.KeyboardButton("Цветы"), types.KeyboardButton("Медицина"), types.KeyboardButton("Развлечение"), types.KeyboardButton("Стоп"))
        rmk.add(types.KeyboardButton("Поесть" + emoji.emojize(':fork_and_knife_with_plate:')), 
        types.KeyboardButton("Красота" + emoji.emojize(':lipstick:')), 
        types.KeyboardButton("Цветы" + emoji.emojize(':bouquet:')), 
        types.KeyboardButton("Медицина" + emoji.emojize(':lab_coat:')), 
        types.KeyboardButton("Развлечение" + emoji.emojize(':confetti_ball:')), 
        types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))
        config.bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=rmk)

        config.bot.register_next_step_handler(message,get_category)
    else:
        config.bot.send_message(message.from_user.id, "Не коректный ввод! Повторите попытку.")
        config.bot.register_next_step_handler(message,get_type)


def get_category(message):
    
    category = message.text


    if(category == 'Стоп' + emoji.emojize(':raised_hand:')):
        stop_newpp(message.from_user.id)
        return

    if category in list_category.keys():
        print(list_category[category])
        placescategory.pc_dictionary[message.from_user.id].append(str(list_category[category]))
        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, "Отправьте фото.", reply_markup=key_stop)
        config.bot.register_next_step_handler(message,save_photo)
    else:
        config.bot.send_message(message.from_user.id,"Введите название категории!")
        config.bot.register_next_step_handler(message, get_category) 

def convertData(filename):
   
    # Convert images or files data to binary format
    with open(filename, 'rb') as file:
        binary_data = file.read()
     
    return binary_data

@config.bot.message_handler(content_types=['photo'])
def save_photo(message):
    # создадим папку если её нет
    Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)
    file_info = None

    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        stop_newpp(message.from_user.id)
    elif not message.photo:
        config.bot.send_message(message.from_user.id, "Отправьте фото.", reply_markup=key_stop)
        config.bot.register_next_step_handler(message,save_photo)
    else:
    # сохраним изображение
        file_info = config.bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = config.bot.download_file(file_info.file_path)
        src = f'files/{message.chat.id}/' + file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        with open(src, 'rb') as file:
            binary_data = file.read()
        places_photo.photo_dictionary[message.from_user.id].append(src)
        places_photo.photo_dictionary[message.from_user.id].append(binary_data)
        
        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, "Укажите соц-сеть.", reply_markup=key_stop)
        config.bot.register_next_step_handler(message,get_email)

    
def get_email(message):
    
    if(message.text == 'Стоп' + emoji.emojize(':raised_hand:')):
        stop_newpp(message.from_user.id)
    elif validation.validationText(message.text):
        places_base.pps_dictionary[message.from_user.id].append(message.text)
        
        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, "Проверьте введенные данные:",reply_markup=del_keyb)
        
        result = get_data_dict(message.from_user.id)
        result += "Если данные верны, нажмите кнопку опубликовать!\nИначе отменить."
        
        print(result + "\n")

        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Опубликовать', callback_data='public')
        keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='Отменить', callback_data='canc_new')
        keyboard.add(key_no)

        config.bot.send_message(message.from_user.id, text=result, reply_markup=keyboard)
    else:
        config.bot.send_message(message.from_user.id, "Не коректный ввод! Повторите попытку.")
        config.bot.register_next_step_handler(message,get_email)


@config.bot.callback_query_handler(func=lambda call: call.data.startswith('public')) 
def callback_people_public(call):

    try:
        if places_base.pps_dictionary.get(call.from_user.id) != None and placescategory.pc_dictionary.get(call.from_user.id) != None:
            print(call.from_user.id)
            print(placescategory.pc_dictionary)
            user_id = call.from_user.id
            user_id_cat = call.from_user.id
            type_work = places_base.pps_dictionary[call.from_user.id][0]
            number_phone = places_base.pps_dictionary[call.from_user.id][1]
            location = places_base.pps_dictionary[call.from_user.id][2]
            about = places_base.pps_dictionary[call.from_user.id][3] 
            time_work = places_base.pps_dictionary[call.from_user.id][4]
            email = places_base.pps_dictionary[call.from_user.id][5]
            category = placescategory.pc_dictionary[call.from_user.id][0]
            photo = places_photo.photo_dictionary[call.from_user.id][0]
            photo_blob = places_photo.photo_dictionary[call.from_user.id][1]
            print(placescategory.pc_dictionary)
            print(places_photo.photo_dictionary)
            

            val = (user_id, type_work,number_phone,location,about,time_work,email)
            valc = (user_id, str(user_id_cat), category)
            val_photo = (str(user_id_cat), user_id, photo_blob, str(photo))
            print(valc)

            places_base.add_places(val)
            placescategory.add_category(valc)
            places_photo.add_photo(val_photo)
            
            result = get_data_dict(call.from_user.id)
            places_photo.print_photo(str(call.from_user.id))

            places_photo.photo_dictionary.pop(call.from_user.id)
            placescategory.pc_dictionary.pop(call.from_user.id)
            places_base.pps_dictionary.pop(call.from_user.id)
            

            config.bot.send_photo(chat_id=call.from_user.id, photo=open(photo, 'rb'), caption=result)

    except:
            config.bot.delete_message(call.message.chat.id, call.message.message_id)
            config.bot.send_message(call.message.chat.id, "Извините, произошел сбой. Повторите попытку")

    config.bot.edit_message_text(call.message.text, chat_id=call.from_user.id, message_id=call.message.message_id)

    
    
@config.bot.callback_query_handler(func=lambda call: call.data.startswith('canc_new')) 
def callback_people_cancel_new(call):
    
    result = get_data_dict(call.from_user.id)
    
    if(result != None):
        places_base.pps_dictionary.pop(call.from_user.id)
        placescategory.pc_dictionary.pop(call.from_user.id)
        config.bot.send_message(call.message.chat.id, "Данные не сохранены!\nПовторить попытку /newpp")
        
    config.bot.edit_message_text(call.message.text, chat_id=call.from_user.id, message_id=call.message.id)
    

def get_data_dict(id_u: int):
    result = None

    if places_base.pps_dictionary.get(id_u) != None and placescategory.pc_dictionary.get(id_u) != None:
        print(id_u)
        result = "Название компании: " + places_base.pps_dictionary[id_u][0] + "\n\n"
        result += "Номер телефона: " + places_base.pps_dictionary[id_u][1] + "\n\n"
        result += "Локация: " + location.get_address_from_coords(places_base.pps_dictionary[id_u][2]) + "\n\n"
        result += "Описание: " + places_base.pps_dictionary[id_u][3] + "\n\n"
        result += "Время работы: " + places_base.pps_dictionary[id_u][4] + "\n\n"
        result += "Соц-сеть: " + places_base.pps_dictionary[id_u][5] + "\n\n"
        result += "Категория: " + placescategory.pc_dictionary[id_u][0] + "\n\n"

 
    return result

def stop_newpp(user_id: int):
    del_keyb = types.ReplyKeyboardRemove()
    config.bot.send_message(user_id, "Остановил.",reply_markup=del_keyb)
    