from django.db import models
from django.contrib.auth.models import User
import uuid

ENABLED = 'ENABLED'
DISABLED = 'DISABLED'

STATUS_CHOICES = (
   (ENABLED, 'Enabled'),
   (DISABLED, 'Disabled')
)

class Wallet(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	owned_by = models.ForeignKey(User,on_delete=models.CASCADE)   
	status = models.CharField(choices=STATUS_CHOICES, max_length=128, default=DISABLED)
	enabled_at = models.DateTimeField()
	balance = models.IntegerField()     

	class Meta:
		db_table = "wallet"


class Withdrawal(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	withdrawn_by = models.ForeignKey(User,on_delete=models.CASCADE) 
	wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)    
	status = models.CharField(max_length=100)
	withdrawn_at = models.DateTimeField()
	amount = models.IntegerField()   
	reference_id = models.CharField(max_length=500) 

	class Meta:
		db_table = "withdrawal"


class Deposit(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	deposited_by = models.ForeignKey(User,on_delete=models.CASCADE)
	wallet = models.ForeignKey(Wallet,on_delete=models.CASCADE)   
	status = models.CharField(max_length=100)
	deposited_at = models.DateTimeField()
	amount = models.IntegerField()   
	reference_id = models.CharField(max_length=500) 

	class Meta:
		db_table = "deposit"