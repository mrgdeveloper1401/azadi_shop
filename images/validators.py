from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from django.core.validators import FileExtensionValidator


def validate_image_size(value):
    max_size = 15
    if value.size > max_size * 1024 * 1024:
        raise ValidationError(_(f"File can't be larger than {max_size} MB"))
    return value
