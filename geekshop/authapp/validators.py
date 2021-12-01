from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class NumberValidator(object):
    def __init__(self, min_digits=1):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_digits:
            raise ValidationError(
                _("The password must contain at least %(min_digits)d digit(s), 0-9."),
                code='password_no_number',
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_digits)d digit(s), 0-9." % {'min_digits': self.min_digits}
        )


def clean_firstname(value):
    errors = []
    errors_status = 0

    if value == '111':
        errors_status = 1
        error = ValidationError(_('Firstname cannot contains 111.'))
        # raise ValidationError(_('Firstname cannot contains 111.'))
        errors.append(error)

    if not value.isalpha():
        errors_status = 1
        error = ValidationError(_('Firstname cannot contains digits.'))
        # raise ValidationError(_('Firstname cannot contains digits.'))
        errors.append(error)

    if errors_status:
        raise ValidationError(errors)
