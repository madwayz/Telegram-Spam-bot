from src.base.database import Database


class Account:
    def __init__(self, account_type):
        self._account = None
        self.account_type = account_type
        self.db = Database()
        self.fetch()

    def fetch(self):
        self._account = self.db.get_current_account(self.account_type)
        self._account['type'] = 'Инвест' if self._account['type'] else 'HR'

    def get_chats(self):
        response = self.db.get_chats_list(account_type=self.account_type)
        return list(map(lambda x: x.get('name'), response))

    def add_chat_list(self, data):
        for chat_id in data:
            self.db.add_chat_id(account_type=self.account_type, chat_id=chat_id)

    def add_chat_name(self, chat_id):
        self.db.add_chat_id(account_type=self.account_type, chat_id=chat_id)

    def get(self):
        return self._account

    def create(self, phone_number, account_type, security_code):
        self.db.add_user(phone_number=phone_number, account_type=account_type, security_code=security_code)

    def count_all(self):
        return self.db.get_account_quantity(self.account_type)
