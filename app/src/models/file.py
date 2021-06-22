from src.models.chat import Chat
from src.utils.excel_builder import XLSXBuilder


class ChatsFile:
    def __init__(self, account_type=None):
        self.account_type = account_type
        self.chat = None

    def get_file(self):
        self.chat = Chat(self.account_type)

        chats_list = self.chat.get_chats()

        document = XLSXBuilder()
        return document.create_file(chats_list)

    @staticmethod
    def parse_file(path):
        document = XLSXBuilder(path)
        return document.parse_file()


