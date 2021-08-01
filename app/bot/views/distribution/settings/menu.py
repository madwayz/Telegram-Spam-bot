from bot.views.distribution.settings.keyboards import get_delivery_settings_keyboard
from bot.views.distribution.settings.keyboards import get_chat_settings_keyboard


class DeliverySettingsMenu:
    def __init__(self, account):
        self.account = account

    @staticmethod
    def get_text():
        return "Желаете настроить отправку сообщений в конкретный чат? " \
               "выберите чат из списка или введите его @username ниже"

    def get_keyboard(self):
        return get_delivery_settings_keyboard(self.account)


class ChatSettings:
    def __init__(self, settings):
        self.settings = settings

    def get_text(self):
        message_quantity = self.settings['message_quantity'] or 'не установлено'
        message_interval = self.settings['message_interval'] or 'не установлено'
        return f"Чат: @{self.settings.get('chat_name')}\n" \
               f"Количество сообщений: {message_quantity}\n" \
               f"Интервал(мин): {message_interval}"

    def get_keyboard(self):
        return get_chat_settings_keyboard(self.settings)
