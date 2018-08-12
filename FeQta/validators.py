from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from .models import Topic


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


def validate_email(value):
    if 'edu' in value:
        raise ValidationError('Edu emails not accepted')

# Categories = ['Mexican','Asian']
#
# def validate_cat(value):
#     cat=value.capitalize()
#     if not value in Categories and not cat in Categories:
#         raise ValidationError('Invalid Category')
# in forms.py category=forms.CharField(required='False',validators=[validate_cat])
# or directly add it in models

# qs = Topic.objects.all()
#
#
# def validate_topic(value):
#     if not value in qs:
#         raise ValidationError(f'{value} Topic does not exist')
