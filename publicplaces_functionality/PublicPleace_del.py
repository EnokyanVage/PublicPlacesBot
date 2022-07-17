from telebot import types
import emoji

from data import config
from database import places_base


del_keyb = types.ReplyKeyboardRemove()

dictionary_del = {}

def del_places(message):
    flag_number = True
    number = 0

    if message.text == 'Стоп' + emoji.emojize(':raised_hand:'):
        config.bot.send_message(message.from_user.id,"Остановил.",reply_markup=del_keyb)
        return

    try:
        number = int(message.text) 
    except Exception:
        flag_number = False
        config.bot.send_message(message.from_user.id, "Цифрами, пожалуйста")
        number = int(0)

    if number > 0 and flag_number == True:
        contact = places_base.get_my_pp_id(message.from_user.id,number)

        if contact == False:
            config.bot.send_message(message.from_user.id, "Общественное место с таким номером не найдено!\nПовторите попытку.")
            config.bot.register_next_step_handler(message, del_places)
        else:
            dictionary_del[message.from_user.id] = []
            dictionary_del[message.from_user.id].append(number)

            keyboard = types.InlineKeyboardMarkup()
            key_del = types.InlineKeyboardButton(text='Удалить', callback_data='delw')
            keyboard.add(key_del)
            key_leav= types.InlineKeyboardButton(text='Оставить', callback_data='leave')
            keyboard.add(key_leav)
            config.bot.send_message(message.from_user.id, contact, reply_markup=keyboard)

    else:
        config.bot.send_message(message.from_user.id, "Общественное место с таким номером не найдено!\nПовторите попытку.")
        config.bot.register_next_step_handler(message, del_places)


@config.bot.callback_query_handler(func=lambda call: call.data.startswith('delw')) 
def callback_people_save(call):

    places_base.del_places(dictionary_del[call.from_user.id][0],call.from_user.id)    
    
    config.bot.delete_message(call.message.chat.id, call.message.message_id)
    dictionary_del.pop(call.from_user.id)
    config.bot.send_message(call.from_user.id, "Удалено.", reply_markup=del_keyb)

     
@config.bot.callback_query_handler(func=lambda call: call.data.startswith('leave')) 
def callback_people_cancel(call):
    
    config.bot.delete_message(call.message.chat.id, call.message.message_id)
    dictionary_del.pop(call.from_user.id)
    config.bot.send_message(call.from_user.id, "Ок.", reply_markup=del_keyb)
        