from django.contrib.auth.decorators import user_passes_test
from users.models import User


def restrict_access(function=None, user_types=[]):
    actual_decorator = user_passes_test(lambda u: u.user_type in user_types)
    if function:
        return actual_decorator(function)

    return actual_decorator
