from django.contrib.auth.models import User
from django.db import OperationalError


def get_standard_user() -> int:
    """
    Returns the standard user right now, just the "first" user
    """
    # We need to use pk because otherwise migrations will fail (ValueError: Cannot serialize: <User: admin>)
    try:
        return User.objects.first().pk
    except (AttributeError, OperationalError):
        return 0
