import logging
import os

from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import send_mail

from celery import shared_task

logger = logging.getLogger('django')


@shared_task
def send_welcome_email(data: dict) -> None:
    """Sends welcome email to user.

    Args:
        data: A dictionary with user data.
    """
    send_email = str(os.getenv("SEND_EMAIL")).lower()
    if not send_email == 'true' or send_email == '1':
        return None

    subject = 'Thanks for registering on Sakuras Sweets!'
    email = data['user_email']
    user = email.split('@')[0]
    website_url = 'https://sakurassweets.asion.dev/'
    email_template = render_to_string('user/user_welcome_email.html', {
        "user": user,
        "website_url": website_url
    })
    try:
        logger.info(f"Email sent to: {email}")
        send_mail(
            subject,
            '',
            'Sakuras Sweets',
            [email],
            fail_silently=False,
            html_message=email_template
        )
    except Exception as e:
        logger.exception(f"Error sending email to {email}: {e}")


@shared_task
def hash_password(password: str) -> str:
    return make_password(password)
