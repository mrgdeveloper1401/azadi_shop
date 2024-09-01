from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import re


class MobileValidator(RegexValidator):
    regex = r"\+?[0-9]{10,15}$"
    message = _(
        'enter a valid mobile number this value contain only number and +'
        'for example +989171234567 or 9171234567 or 09171234567'
    )
