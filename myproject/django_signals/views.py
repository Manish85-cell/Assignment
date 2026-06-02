from django.shortcuts import render
import time
from django.http import HttpResponse
from .models import Person, Product, AuditLog
import threading
from django.db import transaction
# Create your views here.

def test_sync(request):
    print(f"[Caller] running on Thread : {threading.current_thread().name}")
    start = time.time()
    Person.objects.create(name="Manish")
    Product.objects.create(name="Macbook", price=120000)
    end = time.time()
    print(f"Request completed in {end-start:.2f} seconds")
    return HttpResponse(
        f"Request completed in {end-start:.2f} seconds"
    )

def test_transaction(request):
    print("1. Before entering transaction")
    print(
        f"Persons={Person.objects.count()}, "
        f"AuditLogs={AuditLog.objects.count()}"
    )
    try:
        with transaction.atomic():
            print("2. Inside transaction, before Person creation")
            Person.objects.create(name="Sumit")
            print("3. Back in caller after Person creation")
            print(
                f"Persons={Person.objects.count()}, "
                f"AuditLogs={AuditLog.objects.count()}"
            )
            raise Exception("Force rollback")
    except Exception:
        print("4. Exception raised -> Transaction rolled back")
    
    print("5. After transaction block")

    print(
        f"Persons={Person.objects.count()}, "
        f"AuditLogs={AuditLog.objects.count()}"
    )
    
    return HttpResponse("Done")