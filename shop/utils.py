from decouple import config
from requests import post

base_url = 'https://panel.spotplayer.ir/license/edit/'
api_key = config('SPOT_API_KEY', cast=str)


def create_token(mobile_phone, course, name):
    params = {
        "test": True,
        "course": course,
        "name": name,
        "watermark": {"texts": [{"text": mobile_phone}]}
    }
    headers = {
        '$API': api_key,
        '$LEVEL': '-1',
    }
    try:
        response = post(base_url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        raise e
