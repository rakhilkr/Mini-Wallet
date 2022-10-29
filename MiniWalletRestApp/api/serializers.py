from rest_framework import serializers #importing restfrmaework
from .models import * # importing modeles we created
import datetime


class WalletSerializer(serializers.ModelSerializer):

	user = serializers.CharField(source='owned_by.username')

	class Meta:
		model = Wallet
		fields = ['id','user','status','enabled_at','balance']

