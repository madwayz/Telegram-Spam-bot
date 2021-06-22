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

    def get(self):
        return self._account

    def count_all(self):
        return self.db.get_account_quantity(self.account_type)