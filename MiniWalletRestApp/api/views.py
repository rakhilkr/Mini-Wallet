from django.shortcuts import render
from django.http import HttpResponse,Http404 # witten httpresponse
from django.shortcuts import get_object_or_404 # 404 if object is not exists
from rest_framework.views import APIView # normal view can written API data
from rest_framework.response import Response # get a perticular response every thing is okey then give 200 response
from rest_framework import status # basically sent back status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny ,IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
        		token = Token.objects.filter(user=invgltr).first().key
        		return Response(
	                {
	                    "data": {
	                        "token": str(token)
	                    },
	                    "status": "success"
	                },
	                template_name=None
	            )
        	else:
        		return Response(
	                {
	                    "data": {},
	                    "status": "error"
	                },
	                template_name=None
	            )
        except Exception as e:
        	logger.error(e,exc_info=True)
        	return Response(
                {
                    "data": {},
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                template_name=None
            )