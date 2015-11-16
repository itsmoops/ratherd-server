from django.contrib.auth.models import User
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from account.serializers import UserSerializer
from rest_framework import viewsets, permissions, authentication, generics, parsers, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ValidationError
import serializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route()
    def current(self, request):
        userid = request.query_params.get('u', None)
        if userid:
            queryset = User.objects.filter(id=userid)
        else:
            queryset = User.objects.filter(id=1)
        print userid
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print UserSerializer(user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


    obtain_auth_token = ObtainAuthToken.as_view()