from django.urls import path,include
from .views import *

urlpatterns = [
    #-------------Mini Wallet URL's----------------------------------------------------#
    path('v1/init', InitializeWallet.as_view(), name="api-init"),
]