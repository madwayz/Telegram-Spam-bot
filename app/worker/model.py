import os
import typing
import asyncio

import telethon
from telethon import TelegramClient

from worker.config import SESSION_DIR


class UserBot:
    def __init__(self):
        self.client: typing.Union[TelegramClient, None] = None
        self.api_id: typing.Union[str, int, None] = None
        self.api_hash: typing.Union[str, None] = None
        self.phone_number: typing.Union[str, None] = None
        self.session_path: typing.Union[str, None] = None

    def __del__(self):
        if isinstance(self.client, TelegramClient):
            self.client.disconnect()

    def add_api_id(self, api_id):
        self.api_id = api_id

    def add_api_hash(self, api_hash):
        self.api_hash = api_hash

    def add_phone_number(self, phone_number):
        self.phone_number = phone_number

    def _create_client(self):
        self.client = TelegramClient(
            self.session_path,
            self.api_id,
            self.api_hash,
        )

    async def send_code_request(self, session_name=None):
        self.session_path = os.path.join(SESSION_DIR, session_name or os.urandom(7).hex())
        self._create_client()

        await self.client.connect()
        if await self.client.is_user_authorized():
            return {"ok": 'UserAlreadyAuthorized'}

        try:
            await self.client.send_code_request(self.phone_number)
        except telethon.errors.rpcerrorlist.FloodWaitError as e:
            return {"error": 'FloodWaitError', 'seconds': e.seconds}

        return {"ok": "SendCodeSuccessfully"}

    async def reset(self):
        if await self.client.is_user_authorized():
            await self.client.disconnect()

        self.client = None
        self.api_id = None
        self.api_hash = None
        self.phone_number = None

    async def sign_in(self, code):
        await self.client.sign_in(phone=self.phone_number, code=code)

    async def get_me(self):
        return await self.client.get_me()

    def get_session_path(self):
        return self.session_path + '.session'

    def preconfigure(self, api_id, api_hash, phone_number, session_path):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_path = session_path

        self._create_client()

    async def start_distribution(self, chats_list: list, text: str):
        try:
            for chat in chats_list:
                quantity = chat.get('message_quantity')
                interval = chat.get('message_interval')
                chat_name = chat.get('chat_name')
                for _ in range(quantity):
                    await self.client.send_message(chat_name, message=text)
                await asyncio.sleep(interval*60)
            return True
        except:
            return False
