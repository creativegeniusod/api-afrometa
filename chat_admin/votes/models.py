from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


""" Voting Table """
class SiteVote(models.Model):
	page = models.TextField(blank=False, default="invalid page")
	domain = models.TextField(blank=False, default="not a domain")
	vote = models.BooleanField(default=False, blank=False)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.page

