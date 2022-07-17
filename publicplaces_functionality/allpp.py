
from telebot import types
from telegram_bot_pagination import InlineKeyboardPaginator
import emoji

from database import places_base
from data import config
from database import places_photo


del_keyb = types.ReplyKeyboardRemove()


def send_character_page(message, page=1):
        character_pages = places_base.get_pages()
        id = places_base.get_my_id()
        
        photo = places_photo.print_photo(*id[page-1])
        print(photo)
        paginator = InlineKeyboardPaginator(
                len(character_pages),
                current_page=page,
                data_pattern='character#{page}'
        )
       
        config.bot.send_photo(chat_id=message.chat.id, photo=open(photo, 'rb'), caption=character_pages[page-1],reply_markup=paginator.markup)
        

@config.bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='character')
def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    
    config.bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    send_character_page(call.message, page)


def get_pp(message):
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
        contact = places_base.get_contact(number)

        if contact == False:
                config.bot.send_message(message.from_user.id, "PublicPlace с таким номером не найдено!\nПовторите попытку.")
                config.bot.register_next_step_handler(message, get_pp)
        else:
                config.bot.send_message(message.from_user.id, contact, reply_markup=del_keyb)

    else:
        config.bot.send_message(message.from_user.id, "PublicPlace с таким номером не найдено!\nПовторите попытку.")
        config.bot.register_next_step_handler(message, get_pp)
        