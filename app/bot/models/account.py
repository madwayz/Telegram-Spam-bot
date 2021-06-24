from bot.base.database import Database


class Account:
    def __init__(self, account_type=None):
        self._account = None
        self.account_type = account_type
        self.db = Database()

    def _fetch(self):
        self._account = self.db.get_current_account(self.account_type)
        self._account['type'] = 'Инвест' if self._account['type'] else 'HR'

    def get_chats(self):
        response = self.db.get_chats_list(account_type=self.account_type)
        return list(map(lambda x: x.get('name'), response))

    def add_chat_list(self, data):
        for chat_name in data:
            if self.hash_chat_in_list(chat_name):
                continue

            self.db.add_chat_name(account_type=self.account_type, chat_name=chat_name)

    def get_ready_chats_settings(self, chat_name):
        """ Возвращает список/конкретный чат подготовленных(-ый) к рассылке чатов пользователя """
        if chat_name:
            return self.db.get_chat_ready_settings(account_type=self.account_type, chat_name=chat_name)
        else:
            return self.db.get_chats_list_ready_settings(account_type=self.account_type)

    def hash_chat_in_list(self, chat_name):
        return bool(self.db.is_chat_in_list(account_type=self.account_type, chat_name=chat_name))

    def add_chat_name(self, chat_name):
        if self.hash_chat_in_list(chat_name):
            return

        self.db.add_chat_name(account_type=self.account_type, chat_name=chat_name)

    def get(self):
        self._fetch()
        return self._account

    def list(self):
        return self.db.get_accounts_list(self.account_type)

    def create(self, phone_number, account_type, api_id, api_hash, session_path):
        self.db.add_user(
            phone_number=phone_number,
            account_type=account_type,
            api_id=api_id,
            api_hash=api_hash,
            session_path=session_path
        )

    def count_all(self):
        return self.db.get_account_quantity(self.account_type)

    def is_exists(self, phone_number):
        return bool(self.db.check_exits(phone_number=phone_number))

    def set_current(self, account_id):
        self.db.set_current_account(account_type=self.account_type, account_id=account_id)

    def update_info(self, **kwargs):
        self.db.update_account_info(account_type=self.account_type, **kwargs)
