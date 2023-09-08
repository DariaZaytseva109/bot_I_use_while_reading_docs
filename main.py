import telebot
from telebot import types
from telebot.types import InlineKeyboardButton
from sqlalchemy.orm import Session
from sqlalchemy import select
from storage import engine, User



API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler()
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Что делаем?')
    markup = types.InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('Ввести новое слово', callback_data='input_new_word')
    button_2 = InlineKeyboardButton('Повторить слова', callback_data='test')
    markup.row(button_1, button_2)
    bot.send_message(message.chat.id, text='Выбери:', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'input_new_word')
def input_new_word(callback_obj):
    #print(callback_obj.__dict__)
    msg = bot.send_message(callback_obj.from_user.id, 'Введите слово')
    bot.register_next_step_handler(msg, set_into_dict)


@bot.message_handler(content_types=['text'])
def set_into_dict(message):
    user_msg = message.text
    bot.reply_to(message, 'Введите значение слова')
    bot.register_next_step_handler(message, set_meaning, word=user_msg)


@bot.message_handler(content_types=['text'])
def set_meaning(message, word):
    word = word
    meaning = message.text
    user_id = message.from_user.id
    session = Session(engine)
    new_word = User(word=word, user_id=user_id, meaning=meaning)
    session.add(new_word)
    session.commit()
    bot.reply_to(message, f'Добавлено слово:  {new_word.word}   со значением   {meaning} ')



@bot.callback_query_handler(func=lambda call: call.data == 'test')
def test(callback_obj):
    session = Session(engine)
    result = select(User).where(User.user_id == callback_obj.from_user.id)
    print(callback_obj.from_user.id)
    for word in session.scalars(result):
        bot.send_message(callback_obj.from_user.id, f' {word.word}  -  {word.meaning}')



bot.infinity_polling()