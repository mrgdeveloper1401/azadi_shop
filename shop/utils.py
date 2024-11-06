from decouple import config
from requests import post

base_url = 'https://panel.spotplayer.ir/license/edit/'
api_key = config('SPOT_API_KEY', cast=str)
url = base_url + api_key


def create_token(mobile_phone, course):
    params = {
        "course": ["5d2ee35bcddc092a304ae5eb"],
        "name": "customer",
        "watermark": {"texts": [{"text": f"{mobile_phone}"}]}
    }
    try:
        response = post(url, params=params)
        return response
    except Exception as e:
        raise e
