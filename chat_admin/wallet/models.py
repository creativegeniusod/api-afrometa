from django.db import models
from djongo.models import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
""" Wallet Table """
class UserWallet(models.Model):
	wallet = models.TextField(blank=False, default="not a wallet id")
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.wallet


class Wallet(models.Model):
    type = models.TextField(blank=False, default="activeType")
    activeType = models.TextField(blank=False, default="default")
    whiteListedNFTaddresses = models.TextField()

    def __str__(self):
        return self.type
