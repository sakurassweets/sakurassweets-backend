from django.utils import timezone


def update_last_login(user) -> None:

    if user:
        user.last_login = timezone.now()
        user.save()
