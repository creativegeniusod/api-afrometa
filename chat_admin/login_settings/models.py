from django.db import models

# Create your models here.
""" Login Settings Table """
class LoginSettings(models.Model):
	name = models.TextField(blank=False, default="not a wallet id")
	status = models.BooleanField(default=False, blank=False)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name
