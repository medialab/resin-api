from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.text import slugify


def send_mail(
    subject,
    message,
    from_email,
    recipient_list,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
    reply_to_list=None,
):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    mail = EmailMultiAlternatives(
        subject, message, from_email, recipient_list, connection=connection
    )
    if reply_to_list:
        mail.reply_to = reply_to_list
    if html_message:
        mail.attach_alternative(html_message, "text/html")

    return mail.send()


def create_slug(first_name, last_name):
    slug = slugify(f"{first_name} {last_name}")
    from annuaire.models import Member

    if Member.objects.filter(slug=slug).exists():
        slug = f"{slug}-{Member.objects.filter(slug__startswith=slug).count() + 1}"

    return slug
