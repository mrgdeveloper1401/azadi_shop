from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class HomeMobileValidator(RegexValidator):
    regex = r'\d{11,15}$'
    message = _("شماره تماس حداقل 11 رقم و حداکثر 15 رقمی میباشد و شامل اعداد هست")
