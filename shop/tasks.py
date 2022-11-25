from celery import shared_task
from shop.models import *
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse


@shared_task(bind=True)
def send_greetings(self, customer_email):
    debug_flag = settings.DEBUG
    recommended_products = Product.objects.filter(recommended=1)[:6]
    html_template = render_to_string("shop/mail/newsletter.html", {'recommended_products': recommended_products, 'newsletter_message':
                                     "Dziękuje za zapisanie się do newslettera, zapoznaj się z najnowszymi produktami w ofercie sklepu", 'customer_email': customer_email, 'debug_flag': debug_flag})
    text_template = strip_tags(html_template)
    email = EmailMultiAlternatives(
        'Atelier Konrada - Dodanie do newslettera',
        text_template,
        settings.EMAIL_HOST_USER,
        [customer_email],
    )
    email.attach_alternative(html_template, "text/html")
    email.fail_silently = True
    email.send()


@shared_task(bind=True)
def send_newsletter(self):
    debug_flag = settings.DEBUG
    emails = Newsletter.objects.all()
    recommended_products = Product.objects.filter(recommended=1)[:6]
    for customer_email in emails:
        html_template = render_to_string("shop/mail/newsletter.html", {
            'recommended_products': recommended_products, 'newsletter_message': "Zapoznaj się z najnowszymi produktami w ofercie sklepu", 'customer_email': customer_email, 'debug_flag': debug_flag})
        text_template = strip_tags(html_template)
        email = EmailMultiAlternatives(
            'Atelier Konrada - Newsletter',
            text_template,
            settings.EMAIL_HOST_USER,
            [customer_email],
        )
        email.attach_alternative(html_template, "text/html")
        email.fail_silently = True
        email.send()


@shared_task(bind=True)
def send_order_details(self, order_number):
    debug_flag = settings.DEBUG
    order = Order.objects.get(order_number=order_number)
    order_status = order.status
    order_details_url = reverse('status', args=[order_number])
    html_template = render_to_string(
        "shop/mail/order.html", {'order_status': order_status, 'order_details_url': order_details_url, 'debug_flag': debug_flag})
    text_template = strip_tags(html_template)
    email = EmailMultiAlternatives(
        'Atelier Konrada - Zamówienie',
        text_template,
        settings.EMAIL_HOST_USER,
        [order.customer_email],
    )
    email.attach_alternative(html_template, "text/html")
    email.fail_silently = True
    email.send()


@shared_task(bind=True)
def send_message(self, email, topic, message):
    html_templete = render_to_string(
        "shop/mail/message.html", {'message_email': email, 'message': message})
    text_template = strip_tags(html_templete)
    email = EmailMultiAlternatives(
        topic,
        text_template,
        settings.EMAIL_HOST_USER,
        ["kuba4742@gmail.com"],
    )
    email.attach_alternative(html_templete, "text/html")
    email.fail_silently = True
    email.send()
