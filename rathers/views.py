from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rathers.serializers import RatherSerializer
from rathers.models import Rather
from rathers.models import Sucks
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from itertools import chain
from operator import attrgetter
from django.db.models import Count
from django.db.models import Sum

# Create your views here.

class RatherViewSet(viewsets.ModelViewSet):
	queryset = Rather.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
	serializer_class = RatherSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	@list_route()
	def comparison(self, request):
		rather1Url = request.query_params.get('r1', None)
		rather2Url = request.query_params.get('r2', None)

		if rather1Url and rather2Url:
			rather1 = self.queryset.get(id=rather1Url)
			rather2 = self.queryset.get(id=rather2Url)
		else:
			if request.user.id is not None:
				user_sucks_ids = Sucks.objects.values_list('rather_id', flat=True).order_by('rather_id')
				rather1 = Rather.objects.filter(active=True).exclude(id__in=user_sucks_ids).order_by('?')[0]
				rather2 = Rather.objects.filter(active=True,ratio__lte=rather1.ratio).order_by('-ratio').exclude(id__in=user_sucks_ids).exclude(id=rather1.id)[0]
			else:
				rather1 = Rather.objects.filter(active=True).order_by('?')[0]
				rather2 = Rather.objects.filter(active=True,ratio__lte=rather1.ratio).order_by('-ratio').exclude(id=rather1.id)[0]


		rathers = Rather.objects.filter(id__in=[rather1.id,rather2.id])

		user_sucks_1 = Sucks.objects.filter(rather_id=rather1.id, user_id=request.user.id).count()
		user_sucks_2 = Sucks.objects.filter(rather_id=rather2.id, user_id=request.user.id).count()

		user_sucks = {
			"rather1": user_sucks_1,
			"rather2": user_sucks_2
		}

		serialized = self.serializer_class(rathers, context={'request': request}, many=True)
		return Response({ "rathers": serialized.data, "user_sucks": user_sucks }, 200)

	@list_route()
	def ranked(self, request):
		sort_type = request.query_params['sort']
		min_total = "20"
		if sort_type == "winner":
			orders = [ '-ratio', '-wins', '-losses']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True).extra(where=["wins + losses > " + min_total])
		elif sort_type == "loser":
			orders = [ 'ratio', '-wins', '-losses']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True).extra(where=["wins + losses > " + min_total])
		elif sort_type == "contested":
			orders = [ '-ratio']
			sortedValues = Rather.objects.order_by('-ratio').filter(active=True,ratio__lte=.5).extra(where=["wins + losses > " + min_total])
		elif sort_type == "plays":
			orders = [ '-total']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True).extra(where=["wins + losses > " + min_total])
		elif sort_type == "newest":
			orders = [ '-date_submitted']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True)
		elif sort_type == "oldest":
			orders = [ 'date_submitted']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True)

		paginator = Paginator(sortedValues, 10)
		page_number = int(request.query_params['page'])
		try:
			page = paginator.page(page_number)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)

		pagination_data = {
			'has_prev': page.has_previous(),
		    'has_next': page.has_next(),
			'current_page': page_number,
		    'total_pages': paginator.num_pages,
			'prev_page': page_number - 1,
		    'next_page': page_number + 1,
			'total_count': paginator.count
		}
		serialized = self.serializer_class(page, context={'request': request}, many=True)
		return Response({"rathers": serialized.data, "pagination": pagination_data}, 200)

	@list_route()
	def user_rathers(self, request):
		sort_type = request.query_params['sort']
		if sort_type == "winner":
			orders = [ '-ratio', '-wins', '-losses']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True,user_id=request.user.id)
		elif sort_type == "loser":
			orders = [ 'ratio', '-wins', '-losses']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True,user_id=request.user.id)
		elif sort_type == "contested":
			orders = [ '-ratio']
			sortedValues = Rather.objects.order_by('-ratio').filter(active=True,ratio__lte=.5,user_id=request.user.id)
		elif sort_type == "plays":
			orders = [ '-total']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True,user_id=request.user.id)
		elif sort_type == "newest":
			orders = [ '-date_submitted']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True,user_id=request.user.id)
		elif sort_type == "oldest":
			orders = [ 'date_submitted']
			sortedValues = Rather.objects.order_by(*orders).filter(active=True,user_id=request.user.id)

		paginator = Paginator(sortedValues, 10)
		page_number = int(request.query_params['page'])
		try:
			page = paginator.page(page_number)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)

		pagination_data = {
			'has_prev': page.has_previous(),
		    'has_next': page.has_next(),
			'current_page': page_number,
		    'total_pages': paginator.num_pages,
			'prev_page': page_number - 1,
		    'next_page': page_number + 1,
			'total_count': paginator.count
		}

		serialized  = self.serializer_class(page, context={'request': request}, many=True)
		return Response({"rathers": serialized.data, "pagination": pagination_data}, 200)

	@detail_route(methods=['POST'], permission_classes=[AllowAny])
	def vote(self, request, pk):
		rather = self.get_object()
		win = request.query_params['win']
		if win == 'true':
			rather.wins += 1
		else:
			rather.losses += 1
		rather.save()
		serialized = self.serializer_class(rather, context={'request': request})
		return Response(serialized.data, 200)

	@detail_route(methods=['POST'])
	def sucks(self, request, pk):
		rather = self.get_object()

		sucks_current_user = Sucks.objects.filter(rather_id=rather.id, user_id=request.user.id).count()
		if sucks_current_user > 0:
			rather.this_sucks -= 1
			Sucks.objects.filter(rather_id=rather.id, user_id=request.user.id).delete()
		else:
			rather.this_sucks += 1
			sucks = Sucks()
			sucks.rather_id = rather.id
			sucks.user_id = request.user.id
			sucks.save()

		sucks_per_rather = Sucks.objects.filter(rather_id=rather.id).count()
		if rather.this_sucks > 50 and rather.ratio < .25:
			rather.active = False
		else:
			rather.active = True
		rather.save()

		serialized = self.serializer_class(rather, context={'request': request})
		return Response(serialized.data, 200)
