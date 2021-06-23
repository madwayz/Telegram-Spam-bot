from bot.models.account import Account
from bot.views.distribution.settings.keyboards import get_delivery_settings_keyboard
from bot.views.distribution.settings.keyboards import get_chat_settings_keyboard


class DeliverySettingsMenu:
    def __init__(self, state):
        self.state = state
        self.account = Account(state.get('type'))

    @staticmethod
    def get_text():
        return "Желаете настроить отправку сообщений в конкретный чат? " \
               "выберите чат из списка или введите его @username ниже"

    def get_keyboard(self):
        return get_delivery_settings_keyboard(self.state)


class ChatSettings:
    def __init__(self, settings):
        self.settings = settings

    def get_text(self):
        return f"Чат: @{self.settings.get('name')}\n" \
               f"Количество сообщений: {self.settings.get('message_quantity', 'не установлено')}\n" \
               f"Интервал(мин): {self.settings.get('message_interval', 'не установлен')}"

    def get_keyboard(self):
        return get_chat_settings_keyboard(self.settings)
