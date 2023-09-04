from telebot.types import User


class Db:
    def __init__(self):
        self.dct = {}


class My_user(User):
    def __init__(self, is_bot, first_name, user_dict):
        self.user_dict = user_dict
        super().__init__(id, is_bot, first_name)


class Word_to_remember:
    def __init__(self, text, meaning, is_remembered=False):
        self.text = text
        self.meaning = meaning
        self.is_remembered = is_remembered


