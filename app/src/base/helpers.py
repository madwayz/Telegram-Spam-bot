from src.utils.account_type import get_account_type_id


async def update_base_state(state, callback_query):
    account_state = await state.get_data()
    if len(['type', 'alias', 'action'] & account_state.keys()) >= 3:
        return

    account_type_data = get_account_type_id(callback_query.data)
    account_type = account_type_data.get('id')
    account_type_alias = account_type_data.get('alias')

    await state.update_data(type=account_type, alias=account_type_alias)