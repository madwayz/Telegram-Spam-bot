import sqlite3
from settings import DATABASE_PATH


class Database:
    def __init__(self):
        self.connect = sqlite3.connect(DATABASE_PATH)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()
        self.cursor.close()

    def _execute(self, query):
        self.cursor.execute(query)
        return [dict(x) for x in self.cursor.fetchall()]

    def get_accounts_quantity(self):
        query = 'SELECT count(*) as count from account'
        return self._execute(query)[0].get('count')

    def get_current_taxi_account(self):
        query = 'SELECT * FROM account WHERE is_current=True AND type=0'
        return self._execute(query)[0]

    def get_current_invest_account(self):
        query = 'SELECT * FROM account WHERE is_current=True AND type=1'
        return self._execute(query)[0]
