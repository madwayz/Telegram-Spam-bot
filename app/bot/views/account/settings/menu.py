from bot.models.account import Account
from bot.views.account.settings.keyboards import get_text_setting_keyboard, get_edit_text_keyboard


class AccountTextSettingsMenu:
    def __init__(self, state):
        self.state = state
        self.account = Account(state.get('type'))

    def get_text(self):
        text = "Текст рассылки на данный момент:\n{distribution_text}"
        return text.format(**self.account.get())

    def get_keyboard(self):
        return get_text_setting_keyboard(self.state)


class EditTextSettingsMenu:
    @staticmethod
    def get_text():
        return "Введите желаемый текст рассылки ниже👇"

    @staticmethod
    def get_keyboard():
        return get_edit_text_keyboard()
