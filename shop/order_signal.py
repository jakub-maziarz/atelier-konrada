from shop.models import Order
from django.dispatch import receiver
from django.db.models.signals import pre_save
from shop.tasks import send_order_details
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION


@receiver(pre_save, sender=Order)
def update_order(sender, instance, **kwargs):
    instance.order_number = "A" + \
        str(instance.transaction_id)[:2] + str(instance.client_id)[:2]
    if (sender.objects.filter(id=instance.id).count() > 0):
        if (sender.objects.get(id=instance.id).status != instance.status):
            send_order_details.delay(instance.order_number)


@receiver(pre_save, sender=Order)
def log_new_order(sender, instance, **kwargs):
    if not Order.objects.filter(id=instance.id):
        LogEntry.objects.log_action(
            user_id=1,
            content_type_id=ContentType.objects.get_for_model(Order).pk,
            object_id=instance.id,
            object_repr=str("Zamówienie: " + instance.order_number),
            action_flag=ADDITION)
