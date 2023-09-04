
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton

from model import Db, Word_to_remember

API_TOKEN = '6474871614:AAESLEJ4U7wQQ9l9DA0r7s-wkuuzF4v1CEc'
bot = telebot.TeleBot(API_TOKEN)
db = Db()


@bot.message_handler()
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Что делаем?')
    markup = types.InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('Ввести новое слово', callback_data='input_new_word')
    button_2 = InlineKeyboardButton('Проверить знания', callback_data='test')
    markup.row(button_1, button_2)
    bot.send_message(message.chat.id, text='Выбери:', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'input_new_word')
def input_new_word(callback_obj):
    #print(callback_obj.__dict__)
    msg = bot.send_message(callback_obj.from_user.id, 'Введите слово')
    bot.register_next_step_handler(msg, set_into_dict)


@bot.message_handler(content_types=['text'])
def set_into_dict(message):
    user_id = message.from_user.id
    user_msg = message.text
    new_word = Word_to_remember(text=user_msg, meaning=None)
    lst = db.dct.get(user_id, [])
    lst.append(new_word)
    db.dct[user_id] = lst
    print(db.dct)
    bot.reply_to(message, 'Введите значение слова')
    bot.register_next_step_handler(message, set_meaning)


@bot.message_handler(content_types=['text'])
def set_meaning(message):
    meaning = message.text
    user_id = message.from_user.id
    db.dct[user_id][-1].meaning = meaning
    print(db.dct)
    bot.reply_to(message, f'Добавлено слово:{db.dct[user_id][-1].text} со значением {meaning}')



@bot.callback_query_handler(func=lambda call: call.data == 'test')
def test(callback_obj):
    print(db.dct[callback_obj.from_user.id])
    whole_dict = [f'{x.text} - {x.meaning}' for x in (db.dct[callback_obj.from_user.id])]

    for w in whole_dict:
        bot.send_message(callback_obj.from_user.id, w)



bot.infinity_polling()