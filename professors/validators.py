from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class NationCodeValidator(RegexValidator):
    regex = r"[0-9]{10}"
    message = _(
        "enter a valid nation code"
        "for example 2360615274"
    )