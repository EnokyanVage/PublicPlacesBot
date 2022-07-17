from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, asin, radians
from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator
import emoji

from data import config
from database import places_base
from auxiliary_files import validation
from auxiliary_files import location

search_dictionary = {}

list_category = {'Поесть' + emoji.emojize(':fork_and_knife_with_plate:'): 1, 'Красота' + emoji.emojize(':lipstick:'): 2, 'Цветы' + emoji.emojize(':bouquet:'): 3, 'Медицина' + emoji.emojize(':lab_coat:'): 4, 'Развлечение' + emoji.emojize(':confetti_ball:'): 5}

key_stop = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_stop.add(types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))

def location_radar(loc1: str, loc2: str):
    if validation.validationGeo(loc1) == False or validation.validationGeo(loc1) == False:
        return -1

    coord1 = loc1.split(',')    
    coord2 = loc2.split(',')

    latitude_1 = float(coord1[0])
    longitude_1 = float(coord1[1])
    latitude_2 = float(coord2[0])  
    longitude_2 = float(coord2[1])

    longitude_1, latitude_1, longitude_2, latitude_2 = map(radians, [longitude_1, latitude_1, longitude_2, latitude_2])

    dlon = longitude_2 - longitude_1 
    dlat = latitude_2 - latitude_1 
    a = sin(dlat/2)**2 + cos(latitude_1) * cos(latitude_2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    res = c * r
    
    return res

def get_category(message):
    
    category = message.text
    # print("Tut4 = ",type(message.from_user.id))
    
    if(category == 'Стоп' + emoji.emojize(':raised_hand:')):
        stop_searchpp(message.from_user.id)
        return

    if category in list_category.keys():
        search_dictionary[message.from_user.id].append(str(list_category[category]))
        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, config.LOCATION, reply_markup = key_stop)
        config.bot.register_next_step_handler(message,get_location)
    else:
        config.bot.send_message(message.from_user.id,"Введите название категории!")
        config.bot.register_next_step_handler(message, get_category) 
        
    
def check_coords(coords:str):
    
    if validation.validationGeo(coords) == False:
        geolocator = Nominatim(user_agent="my_request")
        location = geolocator.geocode(coords)
        try:
            coords = str(location.longitude) +","+ str(location.latitude)
        except Exception:
            coords = " "

    return coords

def get_location(message):

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_searchpp(message.from_user.id)
        return
    # print("Tut3 = ",type(message.from_user.id))
    coords = ""
    # print(message.text)
    if message.text == None:
        current_position = (message.location.longitude, message.location.latitude)
        #создаем строку в виде ДОЛГОТА,ШИРИНА
        coords = f"{current_position[0]},{current_position[1]}"
    else:
        coords = check_coords(message.text)
        # print("COORDS: ",coords)
        
    street = location.get_address_from_coords(coords)
   
    if street == False:
        config.bot.send_message(message.from_user.id, config.ERROR_LOCATION)
        config.bot.send_message(message.from_user.id, config.LOCATION)
        config.bot.register_next_step_handler(message, get_location)
    else:
        key_radius = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_radius.add(types.KeyboardButton("1"),types.KeyboardButton("2"))
        key_radius.add(types.KeyboardButton("5"),types.KeyboardButton("Весь город"))
        key_radius.add(types.KeyboardButton("Стоп" + emoji.emojize(':raised_hand:')))
        search_dictionary[message.from_user.id].append(coords)
        config.bot.send_message(message.from_user.id, "Выберите радиус поиска, либо введите его в ручную (км)", reply_markup = key_radius)
        config.bot.register_next_step_handler(message, get_radius)

def get_radius(message):
    flag_radius = True
    radius = 0
    # print("Tut1 = ",type(message.from_user.id))
    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        stop_searchpp(message.from_user.id)
        return

    try:
        radius = int(message.text)
    except Exception:
        if(message.text != 'Весь город'):
            flag_radius = False
            config.bot.send_message(message.from_user.id, "Цифрами, пожалуйста " + message.text)
            radius = 0
        else:
            radius = 15
    # print("radius = " + str(radius))
    if (radius > 0 and flag_radius == True):
        search_dictionary[message.from_user.id].append(radius)

        del_keyb = types.ReplyKeyboardRemove()
        config.bot.send_message(message.from_user.id, "Осуществляю поиск...",reply_markup = del_keyb)
        send_character_page(message)

        # del_keyb = types.ReplyKeyboardRemove()
    else:
        config.bot.send_message(message.from_user.id, "Радиус введен не корректно!\nПовторите попытку.")
        config.bot.register_next_step_handler(message, get_radius)


def send_character_page(message, page=1):

        result, photo_link = search_process(message.chat.id)

        paginator = InlineKeyboardPaginator(
                len(result),
                current_page=page,
                data_pattern='search_1#{page}'
        )

        config.bot.send_photo(
                chat_id=message.chat.id, 
                photo=open(photo_link[page-1], 'rb'), 
                caption=result[page-1],
                reply_markup=paginator.markup
        )
        
@config.bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='search_1')
def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    # print("162: ",call.message.chat.id)
    # print("172 = ",page)
    config.bot.delete_message(
        call.message.chat.id,
        call.message.message_id
        
    )

    send_character_page(call.message,page)



def search_process(us_id: int):
    public_places = places_base.print_all()

    count_pp = int(0)
    pages = []
    link_photo = []
    # print("US_ID",us_id)
    spisok_pp_resul = "Результат поиска: \n\n"
    for w in public_places:
        radius = location_radar(w[4], search_dictionary[us_id][1])
        print("RADIUS: ",radius)
        if radius != -1 and radius <= search_dictionary[us_id][2] and w[11] == int(search_dictionary[us_id][0]):
            spisok_pp = spisok_pp_resul
            spisok_pp +="Номер - " + str(w[0]) + "\n"
            spisok_pp +="Название компании: " + str(w[2]) + "\n"
            spisok_pp +="Расположение: - " + str(location.get_address_from_coords(w[4])) + "\n\n"
            spisok_pp +="Расстояние до вас: " + str(round(radius,3)) + " км\n\n"
            spisok_pp +="Описание: " + str(w[5]) + "\n\n"
            spisok_pp +="Время работы: " + str(w[6]) + "\n\n"
            spisok_pp +="Соц-сеть: " + str(w[7]) + "\n\n"
            # spisok_pp +="Link: " + str(w[15]) + "\n\n"

            count_pp += 1
            link_photo.append(str(w[16]))
            pages.append(spisok_pp)
        

    if count_pp == 0:
        spisok_pp = spisok_pp_resul
        spisok_pp += "В заданном радиусе, общественных мест не найдено.\n\nПопробуйте увеличить радиус поиска. /searchpp"
        link_photo.append('publicplaces_functionality/nothing_found.png')
        pages.append(spisok_pp)


    return pages, link_photo

def stop_searchpp(user_id: int):
    del_keyb = types.ReplyKeyboardRemove()
    if( search_dictionary.get(user_id) != None):
        search_dictionary.pop(user_id)

    config.bot.send_message(user_id, "Остановил",reply_markup=del_keyb)
