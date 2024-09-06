from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class UppercasePasswordValidator:
    def validate(self, password, user=None):
        if not any(i.isupper() for i in password):
            raise ValidationError(
                _('The password must contain at least one uppercase letter.'),
                code='password_no_uppercase',
            )

    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter.")