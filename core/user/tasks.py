import logging

from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.core.mail import send_mail

from celery import shared_task

logger = logging.getLogger('django')


@shared_task
def send_welcome_email(data: dict) -> None:
    subject = 'Thanks for registering on Sakuras Sweets!'
    email = data['user_email']
    user = email.split('@')[0]
    website_url = 'https://sakurassweets.asion.tk/'
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
        return True
    except Exception as e:
        logger.exception(f"Error sending email to {email}: {e}")
        return False


@shared_task
def hash_password(password: str) -> str:
    hashed_password = make_password(password)
    return hashed_password
