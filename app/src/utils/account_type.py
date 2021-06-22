def get_account_type_id(account_type):
    type_id_schema = [
        {'callbacks_data': ['taxi_delivery_settings', 'taxi_account'], 'data': {'id': 0, 'alias': 'HR'}},
        {'callbacks_data': ['invest_delivery_settings', 'invest_account'], 'data': {'id': 1, 'alias': 'Инвест'}}
    ]

    response = list(filter(lambda item: account_type in item['callbacks_data'], type_id_schema))[0]
    return response.get('data')
