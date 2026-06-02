import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Person, Product, AuditLog

@receiver(post_save, sender=Person)
def slow_signal_creatingPerson(sender, instance, **kwargs):
    print(f"[People] Creation Signal started on Thread: [{threading.current_thread().name}]")
    time.sleep(5)
    print(f"[People] Creation Signal finished on Thread: [{threading.current_thread().name}]")

@receiver(post_save, sender=Product)
def fast_signal_creatingProduct(sender, instance, **kwargs):
    print(f"[Product] Creation Signal started on Thread: [{threading.current_thread().name}]")
    time.sleep(1)
    print(f"[Product] Creation Signal finished on Thread: [{threading.current_thread().name}]")

@receiver(post_save, sender=Person)
@receiver(post_save, sender=Product)
def create_log(sender, instance, **kwargs):
    AuditLog.objects.create(message=f"Created {instance.name}")
    print("Audit log created")