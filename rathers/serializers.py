from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Rather
import math

class RatherSerializer(serializers.ModelSerializer):
	# ratiofly = serializers.SerializerMethodField()
	# def get_ratiofly(self, obj):
	# 	if obj.wins or obj.losses:
	# 		return round(float(obj.wins) / (float(obj.wins) + float(obj.losses)), 2)
	# 	return 0

	class Meta:
		model = Rather
		fields = [
			'id',
			'rather_text',
			'wins',
			'losses',
			'ratio',
			'date_submitted',
			'date_updated'
		]
		read_only_field = ['id']