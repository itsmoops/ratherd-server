from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# # Create your models here.
# class Account(models.Model):
# 	total_rathers = models.IntegerField(default=1)

@receiver(post_save, sender=User)
def create_token_for_user(sender, **kwargs):
	"""
	Create an Account instance for all newly created User instances. We only
	run on user creation to avoid having to check for existence on each call
	to User.save.
	"""
	user, created = kwargs["instance"], kwargs["created"]
	if created:
		# Account.objects.create(user=user, name=user.username)
		Token.objects.create(user=user)

class ResetCodes(models.Model):
	user = models.ForeignKey(User)
	code = models.IntegerField(default=1000)
