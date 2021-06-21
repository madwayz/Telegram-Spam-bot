from src.base.database import Database
from src.menus.account.info.keyboard import get_account_keyboard


class AccountInfoMenu:
    def __init__(self, account_type):
        self.account_type = account_type
        self.account = None
        self.__get_account()

    def get_text(self):
        text = "Данные {type}-аккаунта:\n" \
               "Номер: {phone_number}\n" \
               "Username: @{username}\n" \
               "Имя: {full_name}"
        return text.format(**self.account)

    def __get_account(self):
        db = Database()
        self.account = db.get_current_account(self.account_type)
        self.account['type'] = 'Инвест' if self.account['type'] else 'HR'

    @staticmethod
    def get_keyboard():
        return get_account_keyboard()
