from decouple import config
from requests import post

base_url = 'https://panel.spotplayer.ir/license/edit/'
api_key = config('SPOT_API_KEY', cast=str)


def create_token(mobile_phone, course, name):
    params = {
        "test": True,
        "course": [course],
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


def send_sms(mobile_phone, code):
    u = "https://www.payamak.vip/api/v1/RestWebApi/"
    url = u + "SendBatchSms"
    username = config("SMS_USERNAME", cast=str)
    password = config("SMS_PASSWORD", cast=str)

    data = {
        "userName": username,
        "password": password,
        "fromNumber": "1000809090",
        "toNumbers": mobile_phone,
        "messageContent": f"کاربر گرامی کد تایید شما برابر است با {code}",
        "isFlash": False,
        "sendDelay": 0
    }
    try:
        response = post(url, json=data, headers={'Content-Type': 'application/json'})
        return response
    except Exception as e:
        raise e


# print(send_sms("09210514437", "1234"))
