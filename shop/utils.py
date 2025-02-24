from decouple import config
import aiohttp
import asyncio
import requests

from shop.status_code import MAX_UPLOADING_SIZE

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
        response = requests.post(base_url, json=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        raise e


async def send_sms(mobile_phone, code):
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
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers={'Content-Type': 'application/json'}) as response:
                return await response.json()
    except Exception as e:
        raise e


def image_upload_validator(value):
    max_image_size = 1 * 1024 * 1024
    if value.size > max_image_size:
        raise MAX_UPLOADING_SIZE
    return value
