from telebot import types
import emoji

from data import config
from database import user_base


def del_user(message):
    consent = message.text

    del_keyb = types.ReplyKeyboardRemove()

    if consent == "Да" + emoji.emojize(':check_mark_button:'):
        user_base.delete_user(message.from_user.id)
        config.bot.send_message(message.from_user.id,'Данные удалены из базы! Если хотите возобновить работу с ботом - зарегестрируйтесь, используя команду /reg',reply_markup=del_keyb)
    else:
        config.bot.send_message(message.from_user.id,'Отменено!',reply_markup=del_keyb)
