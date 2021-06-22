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
        if isinstance(row, str) or isinstance(row, int):
            row = (row, )
        self.cursor.execute(query, row)
        response_dict = [dict(x) for x in self.cursor.fetchall()]
        self.connect.commit()
        return response_dict

    def get_account_quantity(self, account_type: int):
        query = f'SELECT count(*) as count from account WHERE is_current=True AND type=?'
        return self._execute(query, account_type)[0].get('count')

    def get_current_account(self, account_type):
        query = f'SELECT * FROM account WHERE is_current=True AND type=?'
        return self._execute(query, account_type)[0]

    def update_account_text(self, account_type, text):
        query = f'UPDATE account SET distribution_text=? WHERE type=? AND is_current=True'
        return self._execute(query, [text, account_type])

    def get_chats_list(self, account_type):
        query = """
            SELECT c.name FROM account_chats ac
            LEFT JOIN account a ON ac.account_id = a.id
            LEFT JOIN chat_list cl ON ac.chat_list_id = cl.list_id
            LEFT JOIN chat c ON cl.chat_id = c.id
            WHERE a.is_current=True AND a.type=?;
        """
        return self._execute(query, account_type)

    def add_chat_id(self, account_type, chat_id):
        query = """
            INSERT INTO chat (name) VALUES (?);
        """
        self._execute(query, chat_id)
        query = """
            WITH get_account_chat_list_id AS (
                SELECT ac.chat_list_id as chat_list_id FROM account_chats ac
                LEFT JOIN account a on ac.account_id = a.id
                WHERE a.is_current=True and a.type=?
                )
            INSERT INTO chat_list (list_id, chat_id)
            VALUES ((SELECT * from get_account_chat_list_id), LAST_INSERT_ROWID());
        """
        return self._execute(query, account_type)

    def get_settings(self, chat_name):
        query = "SELECT * FROM chat WHERE chat.name=?"
        return self._execute(query, chat_name)[0]

    def add_settings(self, chat_name, interval, message_quantity):
        query = "UPDATE chat SET message_interval=?, message_quantity=? WHERE chat.name=?"
        self._execute(query, [interval, message_quantity, chat_name])

    def update_message_interval(self, chat_name, interval):
        query = "UPDATE chat SET message_interval=? WHERE chat.name=?"
        self._execute(query, [interval, chat_name])

    def update_message_quantity(self, chat_name, quantity):
        query = "UPDATE chat SET message_quantity=? WHERE chat.name=?"
        self._execute(query, [quantity, chat_name])

    def add_user(self, phone_number, account_type, security_code):
        query = "INSERT INTO account (phone_number, type, security_code) " \
                "VALUES (?, ?, ?)"
        self._execute(query, [phone_number, account_type, security_code])



