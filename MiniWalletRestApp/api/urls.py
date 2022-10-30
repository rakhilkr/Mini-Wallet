from django.urls import path,include
from .views import *

urlpatterns = [
    #-------------Mini Wallet URL's----------------------------------------------------#
    path('v1/init', InitializeWallet.as_view(), name="api-init"),
    path('v1/wallet', EnableWallet.as_view(), name="api-wallet"),
    path('v1/wallet/deposits', WalletDeposit.as_view(), name="api-wallet-deposits"),
    path('v1/wallet/withdrawals', WalletWithdrawel.as_view(), name="api-wallet-withdraw"),
]