from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class MobileValidator(RegexValidator):
    regex = r"^0\d{10}$"
    message = _(
        'لطفا شماه موبایل معتبر رو وارد نمایید'
        'مثلا 09171234567'
    )

