from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



""" User created Room """
class Room(models.Model):
	name = models.CharField(max_length=200, blank=False)
	room_id = models.CharField(max_length=200, blank=False, unique=True)
	owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	clean_url = models.CharField(max_length=255, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.room_id


""" Room Users """
class RoomUsers(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)


""" Store Room Chat """
class RoomChat(models.Model):
	message = models.TextField(blank=False)
	message_from = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	sent_time = models.DateTimeField(default=timezone.now)
	room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.message
