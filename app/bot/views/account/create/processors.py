from aiogram.dispatcher import FSMContext
import re
from bot.base.objects import dispatcher, userbot
from aiogram import types

from bot.base.states import AccountRegister
from bot.models.account import Account


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountRegister.register_phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not re.findall(r'^\+\d+$', phone_number):
        await message.answer('Номер необходимо в вести по примеру: +73243214243')
        await state.set_state(AccountRegister.register_phone_number)
        return

    account = Account()
    if account.is_exists(phone_number=phone_number):
        await message.answer('Аккаунт с таким номером уже зарегистрирован')
        await state.set_state(AccountRegister.register_phone_number)
        return

    userbot.add_phone_number(phone_number)
    await state.update_data({'phone_number': phone_number})

    await message.answer('Авторизуйтесь на https://my.telegram.org/apps под необходимым аккаунтом, создайте приложение '
                         'и возьмите оттуда данные, которые будут запрошены на следующих этапах.')
    await message.answer('Введите api_id')
    await AccountRegister.register_api_id.set()


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountRegister.register_api_id)
async def process_api_id(message: types.Message, state: FSMContext):
    api_id = message.text
    if not api_id.isdigit():
        await message.answer('api_id должен быть положительным число. Попробуйте ещё раз.')
        await state.set_state(AccountRegister.register_api_id)
        return

    userbot.add_api_id(api_id)
    await state.update_data({'api_id': api_id})

    await message.answer('Введите api_hash')
    await AccountRegister.register_api_hash.set()


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountRegister.register_api_hash)
async def process_api_hash(message: types.Message, state: FSMContext):
    api_hash = message.text

    userbot.add_api_hash(api_hash)
    await state.update_data({'api_hash': api_hash})

    status = await userbot.send_code_request()
    if status.get('error'):
        await message.answer('Введите код подтверждения, который отправил вам телеграм✉️')
        await state.set_state(AccountRegister.register_phone_number)
        await message.answer(f'Аккаунт заблокирован на {status.get("seconds")} секунд. Введите другой номер телефона.')
        return

    await message.answer('Введите код подтверждения, который отправил вам телеграм✉️')
    await AccountRegister.register_security_code.set()


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountRegister.register_security_code)
async def process_security_number(message: types.Message, state: FSMContext):
    code = message.text
    if not re.findall(r'^\d{5}$', code):
        await message.answer('Код должен быть из 5 цифр. Попробуйте ещё раз.')
        await state.set_state(AccountRegister.register_security_code)
        return

    await userbot.sign_in(code)
    await state.update_data({'security_code': code})
    await process_finish_register(message, state)


async def process_finish_register(message: types.Message, state: FSMContext):
    account_state = await state.get_data()

    phone_number = account_state.get('phone_number')
    account_type = account_state.get('type')
    api_id = account_state.get('api_id')
    api_hash = account_state.get('api_hash')

    account = Account(account_type)
    account.create(
        phone_number=phone_number,
        account_type=account_type,
        api_id=api_id,
        api_hash=api_hash,
        session_path=userbot.get_session_path()
    )

    user_info = await userbot.get_me()
    await userbot.client.disconnect()

    full_name = f'{user_info.first_name} {user_info.last_name}'
    account.update_info(full_name=full_name, username=user_info.username)

    await message.answer(f'Готово! {account_state.get("alias")}-аккаунт успешно зарегистрирован👍')
    await message.answer(f'Информация об аккаунте:\n'
                         f'Номер телефона: {phone_number}\n'
                         f'Имя пользователя: {user_info.username or "не установлено"}\n'
                         f'ФИО: {full_name}\n'
                         f'Тип аккаунта: {account_state.get("alias")}\n')

    async with state.proxy() as data:
        data.pop('phone_number')
        data.pop('api_id')
        data.pop('api_hash')
        data.pop('session_path')