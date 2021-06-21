from aiogram import Dispatcher

from src.base.states import ChatSettings
from src.menus.account.chat_settings.processor import process_edit_text_settings


def register_handlers_edit_text(dp: Dispatcher):
    dp.register_message_handler(process_edit_text_settings, state=ChatSettings.waiting_for_text)
