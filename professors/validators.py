from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class NationCodeValidator(RegexValidator):
    regex = r"^\d{10}$"
    message = _(
        "کد ملی باید شامل عدد باشد"
        "برای مثال 1234567890"
    )


def validate_birth_date(value):
    today_date = datetime.now().date()
    birth_date = datetime.strptime(str(value), "%Y-%m-%d").date()
    age = today_date.year - birth_date.year - ((today_date.month, today_date.day) < (birth_date.month, birth_date.day))
    if age < 18:
        raise ValidationError("سن استاد حداقل باید 18 سال باشد")
    return value
