from bot.base.database import Database


class Chat:
    def __init__(self, account_type=None):
        self.account_type = account_type
        self.db = Database()

    def get_settings(self, chat_name):
        settings = self.db.get_settings(account_type=self.account_type, chat_name=chat_name)
        for key in settings.copy():
            if settings[key] is None:
                settings.pop(key)
        return settings

    def add_settings(self, chat_name, interval, message_quantity):
        self.db.add_settings(
            account_type=self.account_type,
            chat_name=chat_name,
            message_interval=interval,
            message_quantity=message_quantity
        )

    def update_message_interval(self, chat_name, interval):
        self.db.update_message_interval(account_type=self.account_type, chat_name=chat_name, message_interval=interval)

    def update_message_quantity(self, chat_name, quantity):
        self.db.update_message_quantity(account_type=self.account_type, chat_name=chat_name, message_quantity=quantity)

    def has_in_list(self, chat_name):
        return bool(self.db.is_chat_in_list(account_type=self.account_type, chat_name=chat_name))
