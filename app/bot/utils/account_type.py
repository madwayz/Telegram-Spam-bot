def get_account_type_id(callback_data):
    type_id_schema = [
        {'callbacks_data': ['taxi_delivery_settings', 'taxi_account'], 'data': {'id': 0, 'alias': 'HR'}},
        {'callbacks_data': ['invest_delivery_settings', 'invest_account'], 'data': {'id': 1, 'alias': 'Инвест'}}
    ]

    response = list(filter(lambda item: callback_data in item['callbacks_data'], type_id_schema))
    return response[0].get('data') if response else None

