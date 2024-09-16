from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class MobileValidator(RegexValidator):
    regex = r"^0[0-9]{10}$"
    message = _(
        'enter a valid mobile number this value contain only number and +'
        'for example 09171234567'
    )
