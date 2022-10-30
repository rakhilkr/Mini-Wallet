from rest_framework import serializers #importing restfrmaework
from .models import * # importing modeles we created
import datetime


class WalletSerializer(serializers.ModelSerializer):

	user = serializers.CharField(source='owned_by.username')

	class Meta:
		model = Wallet
		fields = ['id','user','status','enabled_at','balance']


class DepositSerializer(serializers.ModelSerializer):

	user = serializers.CharField(source='deposited_by.username')

	class Meta:
		model = Deposit
		fields = ['id','user','status','deposited_at','amount','reference_id']


class WithdrawSerializer(serializers.ModelSerializer):

	user = serializers.CharField(source='deposited_by.username')

	class Meta:
		model = Withdrawal
		fields = ['id','user','status','withdrawn_at','amount','reference_id']