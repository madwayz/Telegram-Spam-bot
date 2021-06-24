from bot.models.account import Account
from bot.views.account.info.keyboard import get_account_info_keyboard, get_create_account_keyboard


class AccountInfoMenu:
    def __init__(self, state):
        self.account = Account(state.get('type'))

    def get_text(self):
        account_data = self.account.get()
        text = f"Данные {account_data.get('type')}-аккаунта:\n" \
               f"Номер: {account_data.get('phone_number')}\n" \
               f"Username: {account_data.get('username')}\n" \
               f"Имя: {account_data.get('full_name')}"
        return text

    @staticmethod
    def get_keyboard():
        return get_account_info_keyboard()


class NotAvailableAccountsMenu:
    @staticmethod
    def get_text():
        return 'Нет доступных аккаунтов.'

    @staticmethod
    def get_keyboard():
        return get_create_account_keyboard()
