from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
# 	username = models.CharField(max_length=200)
# 	name = models.CharField(max_length=200, default="None")
# 	date_created = models.DateTimeField(auto_now_add=True)
# 	date_updated = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return self.username



class Permission(models.Model):
	name = models.CharField(max_length=20, blank=False, unique=True)
	created_by = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name