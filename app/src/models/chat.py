from src.base.database import Database


class Chat:
    def __init__(self, account_type):
        self.account_type = account_type
        self.db = Database()

    def get_chats(self):
        response = self.db.get_chats(account_type=self.account_type)
        return list(map(lambda x: "@" + x.get('username'), response))

    def add_chat_list(self, data):
        for chat_id in data:
            self.db.add_chat_id(account_type=self.account_type, chat_id=chat_id)

    def add_chat_id(self, chat_id):
        self.db.add_chat_id(account_type=self.account_type, chat_id=chat_id)