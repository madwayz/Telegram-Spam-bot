import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DATABASE


class Database:
    def __init__(self):
        self.connect, self.cursor = self._connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()
        self.cursor.close()

    @staticmethod
    def _connect():
        """
        Метод подключения к бд
        :return:
        """
        config_connect = "dbname='{dbname}' user='{user}' host='{host}' password='{password}' port='{port}'"
        connect = psycopg2.connect(config_connect.format(**DATABASE))
        return connect, connect.cursor(cursor_factory=RealDictCursor)

    def _execute(self, query, row):
        if isinstance(row, str) or isinstance(row, int):
            row = (row, )

        response = None
        try:
            self.cursor.execute(query, row)
            self.connect.commit()
        except psycopg2.Error as e:
            print(e.pgerror)
            print(e.diag.message_primary)
        finally:
            try:
                response = self.cursor.fetchall()
            except:
                pass
        return response

    def get_account_quantity(self, account_type: int):
        query = f'SELECT count(*) as count from account a WHERE a.is_current=True AND a.type=%s'
        return self._execute(query, account_type)[0].get('count')

    def get_current_account(self, account_type):
        query = """
            SELECT a.*, ac.api_hash, api_id FROM account a 
            LEFT JOIN api_credentials ac on a.id = ac.account_id
            WHERE a.is_current=True AND a.type=%s
        """
        return self._execute(query, account_type)[0]

    def update_account_text(self, account_type, text):
        query = f'UPDATE account a SET distribution_text = %s WHERE a.type=%s AND a.is_current=True'
        return self._execute(query, [text, account_type])

    def get_chats_list(self, account_type):
        query = """
            SELECT c.name as chat_name FROM chat c
            LEFT JOIN chat_list cl on c.id = cl.chat_id
            LEFT JOIN account a on cl.id = a.chat_list_id
            WHERE a.type=%s and is_current=True
        """
        return self._execute(query, account_type)

    def add_chat_name(self, account_type, chat_name):
        query = """
            WITH add_chat_id as (
                INSERT INTO chat (name) VALUES (%s) RETURNING id
            )
            INSERT INTO chat_list (id, chat_id)
            VALUES (
                (SELECT chat_list_id FROM account WHERE type=%s AND is_current=True),
                (SELECT id from add_chat_id)
            )
        """
        return self._execute(query, [chat_name, account_type])

    def get_settings(self, account_type, chat_name):
        query = """
            SELECT c.name as chat_name, c.message_quantity, c.message_interval FROM chat c
            LEFT JOIN chat_list cl ON c.id = cl.chat_id
            LEFT JOIN account a ON cl.id = a.chat_list_id 
            WHERE c.name=%s AND a.type=%s AND a.is_current=True"""
        return self._execute(query, [chat_name, account_type])[0]

    def add_settings(self, account_type, chat_name, message_interval, message_quantity):
        query = """
            WITH get_chat_id as (
                SELECT c.id as chat_id
                FROM chat c
                         LEFT JOIN chat_list cl ON c.id = cl.chat_id
                         LEFT JOIN account a ON cl.id = a.chat_list_id
                WHERE c.name = %s
                  AND a.type = %s
                  AND a.is_current = True
            )
            UPDATE chat c
            SET message_interval = %s,
                message_quantity = %s
            WHERE c.id = (select chat_id from get_chat_id)
            """
        self._execute(query, [chat_name, account_type, message_interval, message_quantity])

    def update_message_interval(self, account_type, chat_name, message_interval):
        query = """
            WITH get_chat_id as (
                SELECT c.id as chat_id
                FROM chat c
                         LEFT JOIN chat_list cl ON c.id = cl.chat_id
                         LEFT JOIN account a ON cl.id = a.chat_list_id
                WHERE c.name = %s
                  AND a.type = %s
                  AND a.is_current = True
            )
            UPDATE chat c SET message_interval = %s WHERE c.id = (select chat_id from get_chat_id)
        """
        self._execute(query, [chat_name, account_type, message_interval])

    def update_message_quantity(self, account_type, chat_name, message_quantity):
        query = """
                    WITH get_chat_id as (
                        SELECT c.id as chat_id
                        FROM chat c
                                 LEFT JOIN chat_list cl ON c.id = cl.chat_id
                                 LEFT JOIN account a ON cl.id = a.chat_list_id
                        WHERE c.name = %s
                          AND a.type = %s
                          AND a.is_current = True
                    )
                    UPDATE chat c SET message_quantity = %s WHERE c.id = (select chat_id from get_chat_id)
                """
        self._execute(query, [chat_name, account_type, message_quantity])

    def add_user(self, phone_number, account_type, session_name, api_id, api_hash):
        query = "UPDATE account a SET is_current=False WHERE a.type=%s"
        self._execute(query, account_type)

        query = """
            WITH add_user AS (
                INSERT INTO account (phone_number, type, session_name, is_current) 
                VALUES (%s, %s, %s, true) RETURNING id
            )
            INSERT INTO api_credentials (account_id, api_id, api_hash)
            VALUES ((SELECT id from add_user), %s, %s)
        """
        return self._execute(query, [phone_number, account_type, session_name, api_id, api_hash])

    def check_exits(self, phone_number):
        query = "SELECT count(*) AS count FROM account a WHERE a.phone_number=%s"
        return self._execute(query, phone_number)[0].get('count')

    def is_chat_in_list(self, account_type, chat_name):
        query = """
            SELECT count(c) FROM chat c
            LEFT JOIN chat_list cl ON c.id = cl.chat_id
            LEFT JOIN account a ON cl.id = a.chat_list_id
            WHERE c.name=%s AND a.is_current=True AND a.type=%s
        """
        return self._execute(query, [chat_name, account_type])[0].get('count')

    def get_accounts_list(self, account_type):
        query = """
            SELECT a.*, ac.api_id, ac.api_hash
            FROM account a
            LEFT JOIN api_credentials ac on ac.account_id = a.id
            WHERE a.type=%s AND a.is_current=False
        """
        return self._execute(query, account_type)

    def set_current_account(self, account_type, account_id):
        query = """UPDATE account a SET is_current=False WHERE a.type=%s"""
        self._execute(query, account_type)

        query = """UPDATE account a SET is_current=True WHERE a.id=%s"""
        self._execute(query, account_id)

    def get_chat_ready_settings(self, account_type, chat_name):
        query = """
            SELECT c.name as chat_name, c.message_quantity, c.message_interval FROM chat c
            LEFT JOIN chat_list cl ON c.id = cl.chat_id
            LEFT JOIN account a ON cl.id = a.chat_list_id
            WHERE a.type=%s AND is_current=True
            AND c.message_interval IS NOT NULL AND c.message_quantity IS NOT NULL
            AND c.name=%s
        """
        return self._execute(query, [account_type, chat_name])

    def get_chats_list_ready_settings(self, account_type):
        query = """
            SELECT c.name as chat_name, c.message_quantity, c.message_interval FROM chat c
            LEFT JOIN chat_list cl ON c.id = cl.chat_id
            LEFT JOIN account a ON cl.id = a.chat_list_id
            WHERE a.type=%s AND is_current=True
            AND c.message_interval IS NOT NULL AND c.message_quantity IS NOT NULL
        """
        return self._execute(query, account_type)

    def update_account_info(self, account_type, **kwargs):
        query_substring_list = []
        rows = []

        for k, v in kwargs.items():
            query_substring_list.append(f'{k}=%s')
            rows.append(v)
        rows.append(account_type)
        query_substring = ', '.join(query_substring_list)

        query = f""" 
                UPDATE account a SET {query_substring} WHERE a.type=%s AND a.is_current=True
        """
        return self._execute(query, rows)

    def update_distribution_status(self, account_type, status):
        query = f'UPDATE account a SET in_progress = %s WHERE a.type=%s AND a.is_current=True'
        return self._execute(query, [status, account_type])