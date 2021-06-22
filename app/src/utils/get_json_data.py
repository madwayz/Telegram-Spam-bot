import json


def get_callback_data(data, key):
    try:
        return json.loads(data).get(key)
    except json.decoder.JSONDecodeError:
        return data
