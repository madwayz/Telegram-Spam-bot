from aiogram.dispatcher import FSMContext
import re
from bot.base.objects import dispatcher, userbot
from aiogram import types

from bot.base.states import AccountReauth
from bot.models.account import Account


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=AccountReauth.register_security_code)
async def process_reauth_security_number(message: types.Message, state: FSMContext):
    code = message.text
    if not re.findall(r'^\d{5}$', code):
        await message.answer('Код должен быть из 5 цифр. Попробуйте ещё раз.')
        await state.set_state(AccountReauth.register_security_code)
        return

    await userbot.sign_in(code)
    await state.update_data({'security_code': code})

    await userbot.client.terminate()
    await userbot.client.disconnect()

    await message.answer('Аккаунт успешно переавторизован. Сессия обновлена.')
