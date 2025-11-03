from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def send_mail_on_reset_password(
    subject_template_name,
    email_template_name,
    context,
    from_email,
    to_email,
    html_email_template_name,
):
    subject = render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = render_to_string(email_template_name, context)

    User = get_user_model()
    user = User.objects.get(id=context["user"])

    context["user"] = user

    if html_email_template_name:
        html_body = render_to_string(email_template_name, context)
        send_mail(subject, body, from_email, [to_email], html_message=html_body)
    else:
        send_mail(subject, body, from_email, [to_email])
