from django.shortcuts import render
from django.http import HttpResponse,Http404 # witten httpresponse
from django.shortcuts import get_object_or_404 # 404 if object is not exists
from rest_framework.views import APIView # normal view can written API data
from rest_framework.response import Response # get a perticular response every thing is okey then give 200 response
from rest_framework import status # basically sent back status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny ,IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

from .models import *
from .serializers import *

from datetime import datetime

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
        		return Response(
	                {
	                    "data": {
	                        "token": str(token)
	                    },
	                    "status": "success"
	                },
	            )
        	else:
        		return Response(
	                {
	                    "data": {},
	                    "status": "error"
	                },
	            )
        except Exception as e:
        	logger.error(e,exc_info=True)
        	return Response(
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
			return Response(
                {
                    "data": wallet_data,
                    "status": "success"
                },
            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return Response(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )

	def post(self,request):
		try:
			wallet = Wallet.objects.get(owned_by_id=request.user.id)
			if wallet.status == 'Enabled':
				return Response(
	                {
	                    "data": {},
	                    "status": "Already Enabled"
	                },
	            )
			else:
				wallet.status = 'Enabled'
				wallet.save()
				wallet_data = WalletSerializer(wallet).data
				return Response(
	                {
	                    "data": wallet_data,
	                    "status": "success"
	                },
	            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return Response(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )

	def patch(self, request):
		try:
			wallet = Wallet.objects.get(owned_by_id=request.user.id)
			if request.POST.get('is_disabled') == True:
				wallet.status = 'Disabled'
				wallet.save()
				wallet_data = WalletSerializer(wallet).data
				return Response(
	                {
	                    "data": wallet_data,
	                    "status": "success"
	                },
	            )
			else:
				return Response(
	                {
	                    "data": wallet_data,
	                    "status": "Already Disabled"
	                },
	            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return Response(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )


class WalletDeposit(APIView):

	permission_classes = (IsAuthenticated,)

	def post(self,request):
		try:
			amount = request.POST["amount"]
			reference_id = request.POST["reference_id"]
			dep = Deposit()
			dep.deposited_by_id = request.user.id
			dep.status = 'success'
			dep.deposited_at = datetime.now()
			dep.amount = amount
			dep.reference_id = reference_id
			dep.save()
			deposit_data = DepositSerializer(dep).data
			return Response(
                {
                    "data": deposit_data,
                    "status": "success"
                },
            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return Response(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )


class WalletWithdrawel(APIView):

	permission_classes = (IsAuthenticated,)

	def post(self,request):
		try:
			amount = request.POST["amount"]
			reference_id = request.POST["reference_id"]
			dep = Withdrawal()
			dep.withdrawn_by_id = request.user.id
			dep.status = 'success'
			dep.withdrawn_at = datetime.now()
			dep.amount = amount
			dep.reference_id = reference_id
			dep.save()
			withdraw_data = DepositSerializer(dep).data
			return Response(
                {
                    "data": deposit_data,
                    "status": "success"
                },
            )
		except Exception as e:
			logger.error(e,exc_info=True)
			return Response(
                {
                    "data": {},
                    "status": status.HTTP_403_FORBIDDEN
                },
            )

