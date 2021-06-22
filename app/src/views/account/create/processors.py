from aiogram.dispatcher import FSMContext
import re
from src.base.objects import dispatcher
from aiogram import types

from src.base.states import AccountRegister
from src.models.account import Account


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountRegister.register_phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not re.findall(r'^\+\d+$', phone_number):
        await message.answer('Номер необходимо в вести по примеру: +73243214243')
        await state.set_state(AccountRegister.register_phone_number)
        return

    await state.update_data({'phone_number': phone_number})

    await message.answer('Введите код подтверждения, который отправил вам телеграм✉️')
    await AccountRegister.register_security_code.set()


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountRegister.register_security_code)
async def process_security_number(message: types.Message, state: FSMContext):
    code = message.text
    if not re.findall(r'^\d{5}$', code):
        await message.answer('Неправильный формат кода. Введите ещё раз.')
        await state.set_state(AccountRegister.register_security_code)
        return

    await state.update_data({'security_code': code})
    await process_finish_register(message, state)


async def process_finish_register(message: types.Message, state: FSMContext):
    account_state = await state.get_data()

    phone_number = account_state.get('phone_number')
    security_code = account_state.get('security_code')
    account_type = account_state.get('type')

    account = Account(account_type)
    account.create(phone_number=phone_number, account_type=account_type, security_code=security_code)

    await message.answer(f'Готово! {account_state.get("alias")}-аккаунт успешно зарегистрирован👍')
