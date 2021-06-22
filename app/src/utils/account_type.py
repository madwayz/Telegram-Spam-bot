def get_account_type_id(account_type):
    return {
        'taxi_account': {'id': 0, 'alias': 'HR'},
        'invest_account': {'id': 1, 'alias': 'Инвест'}
    }[account_type]
