from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Rather
import math

class RatherSerializer(serializers.ModelSerializer):

	class Meta:
		model = Rather
		fields = [
			'id',
			'user',
			'rather_text',
			'wins',
			'losses',
			'ratio',
			'date_submitted',
			'date_updated'
		]
		read_only_field = ['id']