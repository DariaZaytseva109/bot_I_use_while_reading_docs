from telebot.types import User


class My_user(User):
    def __init__(self, is_bot, first_name, user_dict):
        self.user_dict = user_dict
        super().__init__(id, is_bot, first_name)






