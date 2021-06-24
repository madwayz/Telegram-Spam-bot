from bot.models.account import Account
from bot.views.account.list.keyboards import get_accounts_list_keyboard


class AccountListMenu:
    def __init__(self, account_state):
        self.state = account_state
        self.account = Account(account_state.get('type'))

    @staticmethod
    def get_text():
        return "Выберите аккаунт из списка."

    def get_keyboard(self):
        return get_accounts_list_keyboard(self.state, self.account)
