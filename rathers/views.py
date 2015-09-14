from rest_framework import viewsets
from django.shortcuts import render
from django.db.models import Sum
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rathers.serializers import RatherSerializer
from rathers.models import Rather
import random

# Create your views here.
class RatherViewSet(viewsets.ModelViewSet):
	queryset = Rather.objects.all()
	serializer_class = RatherSerializer

	@list_route()
	def comparison(self, request):
		rather1 = Rather.objects.order_by('?')[0]
		rather2 = Rather.objects.filter(ratio__lte=rather1.ratio).order_by('-ratio').exclude(id=rather1.id)[0]
		rathers = Rather.objects.filter(id__in=[rather2.id,rather1.id])
		serialized  = self.serializer_class(rathers, context={'request': request}, many=True)
		return Response(serialized.data, 200)

	@list_route()
	def ranked(self, request):
		count = Rather.objects.count()
		top = Rather.objects.order_by('id').extra(where=["wins + losses > 10"])
		serialized = self.serializer_class(top, context={'request': request}, many=True)
		return Response(serialized.data, 200)

	@detail_route(methods=['POST'])
	def vote(self, request, pk):
		rather = self.get_object()
		win = request.query_params['win']
		if win == 'true':
			rather.wins += 1
		else:
			rather.losses += 1
		rather.save()
		serialized  = self.serializer_class(rather, context={'request': request})
		return Response(serialized.data, 200)