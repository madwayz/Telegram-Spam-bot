from bot.utils.account_type import get_account_type_id


async def update_base_state(state, account_type_name):
    account_type_data = get_account_type_id(account_type_name)
    if not account_type_data:
        return

    account_type = account_type_data.get('id')
    account_type_alias = account_type_data.get('alias')

    await state.update_data(type=account_type, alias=account_type_alias)