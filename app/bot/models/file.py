from bot.models.account import Account
from bot.utils.excel_builder import XLSXBuilder


class ChatsFile:
    def __init__(self, account_type=None):
        self.account_type = account_type
        self.account = None

    def get_file(self):
        self.account = Account(self.account_type)

        chats_list = self.account.get_chats()

        document = XLSXBuilder()
        return document.create_file(chats_list)

    @staticmethod
    def parse_file(path):
        document = XLSXBuilder(path)
        return document.parse_file()
