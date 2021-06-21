def get_account_type_id(account_type):
    return {
        'taxi_account': 0,
        'invest_account': 1
    }[account_type]
