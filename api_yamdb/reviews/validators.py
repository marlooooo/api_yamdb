from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    if value < 1000 or value > timezone.now().year:
        raise ValidationError('bad year!')
