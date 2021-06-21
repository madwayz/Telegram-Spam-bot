from src.base.database import Database
from src.menus.account.chat_settings.keyboard import get_text_setting_keyboard, get_edit_text_keyboard


class ChatSettingsMenu:
    def __init__(self, account_type):
        self.account_type = account_type
        self.account = None
        self.__get_account()

    def get_text(self):
        text = "Текст рассылки на данный момент:\n{distribution_text}"
        return text.format(**self.account)

    def __get_account(self):
        db = Database()
        self.account = db.get_current_account(self.account_type)

    @staticmethod
    def get_keyboard():
        return get_text_setting_keyboard()


class EditTextSettingsMenu:
    @staticmethod
    def get_text():
        return "Введите желаемый текст рассылки ниже👇"

    @staticmethod
    def get_keyboard():
        return get_edit_text_keyboard()