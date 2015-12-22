from django.db import models
import pytz
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Rather(models.Model):
	user = models.ForeignKey(User)
	rather_text = models.CharField(max_length=1000)
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)
	ratio = models.DecimalField(default=0.5, max_digits=20, decimal_places=10)
	this_sucks = models.IntegerField(default=0)
	date_submitted = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=1)

	def __str__(self):
		return self.rather_text

	def save(self, *args, **kwargs):
		if self.wins > 0 or self.losses > 0:
			self.ratio = round(float(self.wins) / (float(self.wins) + float(self.losses)), 10)
			self.date_updated = datetime.now(pytz.utc)
		else:
			self.ratio = 0.5
		super(Rather, self).save(*args, **kwargs)

class Sucks(models.Model):
	rather = models.ForeignKey(Rather)
	user = models.ForeignKey(User)
