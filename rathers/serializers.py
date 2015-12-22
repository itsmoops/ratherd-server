from rest_framework import serializers
from account.serializers import ProfileSerializer
from .models import Rather, Sucks
import math


class SucksSerializer(serializers.ModelSerializer):
	class Meta:
		model = Sucks
		field = [
			'rather',
			'user'
		]
		read_only_field = ['id']

class RatherSerializer(serializers.ModelSerializer):
	user = ProfileSerializer(read_only=True, default=serializers.CurrentUserDefault())
	sucks = SucksSerializer(read_only=True)
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
			'sucks',
			'date_submitted',
			'date_updated',
			'active'
		]
		read_only_field = ['id']
