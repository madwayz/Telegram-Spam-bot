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

    def _execute(self, query, row):
        if not hasattr(row, '__iter__'):
            row = (row, )
        self.cursor.execute(query, row)
        response = [dict(x) for x in self.cursor.fetchall()]
        self.connect.commit()
        return response

    def get_account_quantity(self, account_type: int):
        query = f'SELECT count(*) as count from account WHERE is_current=True AND type=?'
        return self._execute(query, account_type)[0].get('count')

    def get_current_account(self, account_type):
        query = f'SELECT * FROM account WHERE is_current=True AND type=?'
        return self._execute(query, account_type)[0]

    def update_account_text(self, account_type, text):
        query = f'UPDATE account SET distribution_text=? WHERE type=? AND is_current=True RETURNING id'
        return self._execute(query, [text, account_type])
