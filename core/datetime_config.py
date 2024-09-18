from jdatetime import datetime, timedelta
from pytz import timezone

now = datetime.now(timezone('Asia/Tehran'))
after_two_minute = now + timedelta(minutes=2)


if __name__ == "__main__":
    print(now)
    print(after_two_minute)
