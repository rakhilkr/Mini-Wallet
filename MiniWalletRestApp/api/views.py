from django.shortcuts import render
from django.http import HttpResponse,Http404 # witten httpresponse
from django.shortcuts import get_object_or_404 # 404 if object is not exists
from rest_framework.views import APIView # normal view can written API data
from rest_framework.response import Response # get a perticular response every thing is okey then give 200 response
from rest_framework import status # basically sent back status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny ,IsAuthenticated
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.utils import timezone

from django.http import JsonResponse

from .models import *
from .serializers import *

import logging,traceback
logger=logging.getLogger(__name__)


class InitializeWallet(APIView):

    permission_classes = (AllowAny,) 

    def post(self,request):
        try:
        	usr = request.POST["customer_xid"]
        	invgltr = User.objects.filter(username=usr).first()
        	if invgltr is not None:
        		user_auth= authenticate(username=request.POST["customer_xid"])
        		login(request, invgltr)
        		token = Token.objects.filter(user=invgltr).first().key
        		return JsonResponse(
	                {
	                    "data": {
	                        "token": str(token)
	                    },
	                    "status": "success"
	                },
	            )
        	else:
        		return JsonResponse(
	                {
	                    "data": {},
	                    "status": "User does not exist."
	                },
	            )
        except Exception as e:
        	logger.error(e,exc_info=True)
        	return JsonResponse(
                {
                    "data": {},
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
            )


class EnableWallet(APIView):

	permission_classes = (IsAuthenticated,)

	def get(self, request):
		try:
			wallet = Wallet.objects.get(owned_by_id=request.user.id)
			wallet_data = WalletSerializer(wallet).data
			return JsonResponse(
                {
                    "data": wallet_data,
                    "status": "success"
                },
            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return JsonResponse(
                {
                    "data": {},
                    "status": 'Sorry, No wallet found.'
                },
            )

	def post(self,request):
		try:
			wallet = Wallet.objects.get(owned_by_id=request.user.id)
			if wallet.status == 'Enabled':
				return JsonResponse(
	                {
	                    "data": {},
	                    "status": "Already Enabled"
	                },
	            )
			else:
				wallet.status = 'Enabled'
				wallet.enabled_at = timezone.now()
				wallet.save()
				wallet_data = WalletSerializer(wallet).data
				return JsonResponse(
	                {
	                    "data": wallet_data,
	                    "status": "success"
	                },
	            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return JsonResponse(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )

	def patch(self, request):
		try:
			wallet = Wallet.objects.get(owned_by_id=request.user.id)
			if request.POST.get('is_disabled') == True and wallet.status == 'Enabled':
				wallet.status = 'Disabled'
				wallet.enabled_at = timezone.now()
				wallet.save()
				wallet_data = WalletSerializer(wallet).data
				return JsonResponse(
	                {
	                    "data": wallet_data,
	                    "status": "success"
	                },
	            )
			else:
				return JsonResponse(
	                {
	                    "data": [],
	                    "status": "Already Disabled"
	                },
	            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return JsonResponse(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )


class WalletDeposit(APIView):

	permission_classes = (IsAuthenticated,)

	def post(self,request):
		try:
			wallet = Wallet.objects.filter(owned_by_id=request.user.id).first()
			if wallet.status == 'Disabled':
				return JsonResponse(
	                {
	                    "data": {},
	                    "status": "Wallet it Disabled, Please Enable it first."
	                },
	            )
			else:
				with transaction.atomic():
					amount = int(request.POST["amount"])
					reference_id = request.POST["reference_id"]
					dep = Deposit()
					dep.deposited_by_id = request.user.id
					dep.status = 'success'
					dep.deposited_at = timezone.now()
					dep.amount = int(amount)
					dep.wallet = wallet
					dep.reference_id = reference_id
					dep.save()
					wallet.balance += int(amount)
					wallet.save()
					deposit_data = DepositSerializer(dep).data
					return JsonResponse(
		                {
		                    "data": deposit_data,
		                    "status": "success"
		                },
		            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return JsonResponse(
                {
                    "data": {},
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
            )


class WalletWithdrawel(APIView):

	permission_classes = (IsAuthenticated,)

	def post(self,request):
		try:
			wallet = Wallet.objects.filter(owned_by_id=request.user.id).first()
			if wallet.status == 'Disabled':
				return JsonResponse(
	                {
	                    "data": {},
	                    "status": "Wallet it Disabled, Please Enable it first."
	                },
	            )
			else:
				with transaction.atomic():
					amount = int(request.POST["amount"])
					reference_id = request.POST["reference_id"]
					if int(request.POST["amount"]) <= wallet.balance:
						dep = Withdrawal()
						dep.withdrawn_by_id = request.user.id
						dep.status = 'success'
						dep.withdrawn_at = timezone.now()
						dep.amount = amount
						dep.reference_id = reference_id
						dep.wallet = wallet
						dep.save()
						wallet.balance -= int(amount)
						wallet.save()
						withdraw_data = WithdrawSerializer(dep).data
						return JsonResponse(
			                {
			                    "data": withdraw_data,
			                    "status": "success"
			                },
			            )
					else:
						return JsonResponse(
							{
			                    "data": {},
			                    "status": "You don't have enough balance."
			                },
			            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return JsonResponse(
                {
                    "data": {},
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
            )

