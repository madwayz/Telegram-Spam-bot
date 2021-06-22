from src.models.account import Account
from src.views.account.info.keyboard import get_account_keyboard


class AccountInfoMenu:
    def __init__(self, state):
        self.account = Account(state.get('type'))

    def get_text(self):
        text = "Данные {type}-аккаунта:\n" \
               "Номер: {phone_number}\n" \
               "Username: @{username}\n" \
               "Имя: {full_name}"
        return text.format(**self.account.get())

    @staticmethod
    def get_keyboard():
        return get_account_keyboard()
