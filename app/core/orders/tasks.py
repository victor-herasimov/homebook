from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from .services import OrderService


@shared_task
def order_create_send_mail_to_client(order_id):
    order = OrderService().get_order_by_id(order_id)

    subject = f"Замовлення №{order.id}"
    message = render_to_string(
        "orders/order/mail/mail_to_client.html", context={"order": order}
    )

    mail_sent = send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=message,
    )
    return mail_sent


@shared_task
def order_create_send_mail_to_staff(order_id):
    order = OrderService().get_order_by_id(order_id)
    User = get_user_model()
    staff_user = User.objects.filter(is_staff=True, is_active=True).first()
    recipient = staff_user.email

    subject = f"Нове замовлення №{order.id}"
    # message = f"Ваше замовлення №{order.id} на суму {order.get_total_cost()} грн створено успішно"
    message = render_to_string(
        "orders/order/mail/mail_to_staff.html", context={"order": order}
    )

    if recipient:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            html_message=message,
        )
