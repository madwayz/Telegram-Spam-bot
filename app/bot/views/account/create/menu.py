from bot.models.account import Account
from bot.views.account.create.keyboard import get_confirm_box_keyboard


class AccounCreateConfirmMenu:
    def __init__(self, state):
        self.account = Account(state.get('type'))

    @staticmethod
    def get_text():
        return "Вы желаете создать новый аккаунт?"

    @staticmethod
    def get_keyboard():
        return get_confirm_box_keyboard()
