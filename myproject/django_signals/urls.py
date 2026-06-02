from django.urls import path
from .views import test_sync, test_transaction

urlpatterns = [
    path("sync/", test_sync),
    path("test_transaction/", test_transaction),
]