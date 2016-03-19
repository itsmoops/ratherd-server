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
from django.core import serializers
from django.core.mail import send_mail

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(permission_classes=[permissions.IsAuthenticated])
    def current(self, request):
        if request.user.is_authenticated():
            serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def send_email(self, request):
        current = User.objects.get(username=request.data["username"])

        body = "Hey " + current.username + ", we got a request to reset your Would You Rather password. Here ya go, idiot!"
        link = "www.wouldyourather.us/resetpw"
        email = current.email

        send_mail('Would You Rather - Password Reset', body, 'info@wouldyourather.us', [email], link, fail_silently=False)
        # serializer = UserSerializer(current)
        return Response(email, 200)

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
        return Response({'token': token.key, 'user': UserSerializer(user).data})

    obtain_auth_token = ObtainAuthToken.as_view()
