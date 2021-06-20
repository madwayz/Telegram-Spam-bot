from src.base.database import Database
from src.menus.account.info.keyboard import get_account_keyboard


class AccountInfoMenu:
    def __init__(self, initiator):
        self.initiator = initiator
        self.account = None
        self.get_account()

    def get_text(self):
        text = "Данные {type}-аккаунта:\n" \
               "Номер: {phone_number}\n" \
               "Username: @{username}\n" \
               "Имя: {full_name}"
        return text.format(**self.account)

    def get_account(self):
        db = Database()
        if self.initiator == 'taxi_account':
            self.account = db.get_current_taxi_account()
        else:
            self.account = db.get_current_invest_account()
        self.account['type'] = 'HR' if self.account['type'] else 'Инвест'

    @staticmethod
    def get_keyboard():
        return get_account_keyboard()
