import os
import typing
import asyncio

from worker.config import SESSION_DIR

from pyrogram import Client


class UserBot:
    def __init__(self):
        self.client: typing.Union[Client, None] = None
        self.api_id: typing.Union[str, int, None] = None
        self.api_hash: typing.Union[str, None] = None
        self.phone_number: typing.Union[str, None] = None
        self.session_name: typing.Union[str, None] = None
        self.phone_code_hash: typing.Union[str, None] = None
        self.account_data = None

    def __del__(self):
        if self.client:
            self.client.terminate()
            self.client.disconnect()

    def add_api_id(self, api_id):
        self.api_id = api_id

    def add_api_hash(self, api_hash):
        self.api_hash = api_hash

    def add_phone_number(self, phone_number):
        self.phone_number = phone_number

    def _set_params(self, kwargs):
        return [setattr(self, attr, value) for attr, value in kwargs.items()]

    def generate_session(self):
        self.session_name = os.urandom(7).hex()

    async def sign_in(self, code):
        await self.client.sign_in(
            phone_number=self.phone_number,
            phone_code_hash=self.phone_code_hash,
            phone_code=code
        )

    async def get_me(self):
        return await self.client.get_me()

    async def send_code(self):
        sent_code = await self.client.send_code(phone_number=self.phone_number)
        self.phone_code_hash = sent_code.__getattribute__('phone_code_hash')

    async def authorize(self, **kwargs):
        status = None
        if kwargs and all(kwargs.values()):
            self._set_params(kwargs)

        if not kwargs.get('session_name'):
            self.generate_session()

        await self.create_client()

        if not kwargs.get('session_name'):
            await self.send_code()
            status = 'SecurityCodeNeeded'

        return status

    async def create_client(self):
        self.client = Client(
            session_name=self.session_name,
            phone_number=self.phone_number,
            api_id=self.api_id,
            api_hash=self.api_hash,
            workdir=SESSION_DIR
        )
        await self.client.connect()
        await self.client.initialize()

    async def send_message(self, chat_name, interval, quantity, text):
        for _ in range(quantity):
            await self.client.join_chat(f'@{chat_name}')
            await self.client.send_message(f'@{chat_name}', text)
            await asyncio.sleep(interval * 60)

    async def create_tasks(self, chats_list, text):
        tasks = []
        for chat in chats_list:
            quantity = chat.get('message_quantity')
            interval = chat.get('message_interval')
            chat_name = chat.get('chat_name')
            task = self.client.loop.create_task(self.send_message(chat_name, interval, quantity, text))
            tasks.append(task)
        return tasks

    async def start_distribution(self, chats_list: list, text: str):
        tasks = await self.create_tasks(chats_list, text)
        await asyncio.wait(tasks)
        await self.client.terminate()
        await self.client.disconnect()
