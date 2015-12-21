from rest_framework import serializers
from django.contrib.auth.models import User
from account.serializers import ProfileSerializer
from .models import Rather
import math

class RatherSerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True,  default=serializers.CurrentUserDefault())
	class Meta:
		model = Rather
		fields = [
			'id',
			'user',
			'rather_text',
			'wins',
			'losses',
			'ratio',
			'this_sucks',
			'date_submitted',
			'date_updated'
		]
		read_only_field = ['id']
