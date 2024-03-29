from bot.models.chat import Chat


async def update_message_interval(message, state):
    interval = message.text
    current_state = await state.get_data()
    chat_name = current_state.get('chat_name')
    account_type = current_state.get('type')

    chat = Chat(account_type=account_type)
    chat.update_message_interval(chat_name=chat_name, interval=interval)


async def update_message_quantity(message, state):
    quantity = message.text
    current_state = await state.get_data()
    chat_name = current_state.get('chat_name')
    account_type = current_state.get('type')

    chat = Chat(account_type=account_type)
    chat.update_message_quantity(chat_name=chat_name, quantity=quantity)
