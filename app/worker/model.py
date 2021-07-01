import os
import typing
import asyncio

import telethon
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

from worker.config import SESSION_DIR


class UserBot:
    def __init__(self):
        self.client: typing.Union[TelegramClient, None] = None
        self.api_id: typing.Union[str, int, None] = None
        self.api_hash: typing.Union[str, None] = None
        self.phone_number: typing.Union[str, None] = None
        self.session_path: typing.Union[str, None] = None
        self.account_data = None

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
        finally:
            await self.client.disconnect()

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

    async def preconfigure(self, api_id, api_hash, phone_number, session_path):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_path = session_path

        self._create_client()
        await self.client.connect()
        self.account_data = await self.client.get_me()

    async def send_message(self, chat_name, interval, quantity, text):
        for _ in range(quantity):
            await self.client(JoinChannelRequest(channel=chat_name))
            await self.client.send_message(chat_name, message=text)
            await asyncio.sleep(interval * 60)

    async def create_tasks(self, chats_list, text):
        tasks = []
        for chat in chats_list:
            quantity = chat.get('message_quantity')
            interval = chat.get('message_interval')
            chat_name = chat.get('chat_name')
            task = self.client.loop.create_task(self.send_message(chat_name, interval, quantity, text), name='test')
            tasks.append(task)
        return tasks

    async def start_distribution(self, chats_list: list, text: str):
        try:
            await self.create_tasks(chats_list, text)
            return True
        except Exception:
            import traceback
            traceback.print_exc()
            return False
