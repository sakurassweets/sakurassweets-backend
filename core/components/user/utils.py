from django.utils import timezone


def update_last_login(user) -> None:

    if user:
        user.last_login = timezone.now()
        user.save()


def clean_error_message(message: str) -> str:
    cleaned_message = [line.strip()
                       for line in message.split('\n') if line.strip()]
    cleaned_message = ' '.join(cleaned_message)
    return cleaned_message
