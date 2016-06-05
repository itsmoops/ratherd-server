from django.contrib.auth.models import User
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from account.serializers import UserSerializer
from account.models import ResetCodes
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
from random import randint
from django.contrib.auth import get_user_model

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
        count = User.objects.filter(username=request.data["username"]).count()

        if count > 0:
            current = User.objects.get(username=request.data["username"])

            codes_current_user = ResetCodes.objects.filter(user_id=current.id).count()
            code = ResetCodes()
            random_num = randint(1000, 9999)
            if codes_current_user > 0:
                ResetCodes.objects.filter(user_id=current.id).delete()
                code.user_id = current.id
                code.code = random_num
                code.save()
            else:
                code.user_id = current.id
                code.code = random_num
                code.save()

            link = "www.ratherd.com/verify?u=" + str(current.id)
            body = "Hey " + current.username + ", we got a request to reset your Rather'd password. Follow the link attached and use the reset code provided here: \n \n" + str(random_num) + "\n \n" + link
            email = current.email
            send_mail("Rather'd - Password Reset", body, "info@ratherd.com", [email], fail_silently=False)

            response = email
        else:
            response = False

        return Response(response, 200)

    @list_route(methods=["POST"])
    def check_code(self, request):
        user_val = request.data["user"]
        code_val = request.data["code"]
        count = ResetCodes.objects.filter(user_id=user_val, code=code_val).count()

        if count > 0:
            current = User.objects.get(id=request.data["user"])
            ResetCodes.objects.filter(user_id=current.id).delete()
            response = UserSerializer(current).data
        else:
            response = False

        return Response(response, 200)

    @list_route(methods=["POST"])
    def update_password(self, request):
        user = User.objects.get(username__exact=request.data["username"])
        user.set_password(request.data["password"])
        user.save()

        response = UserSerializer(user).data

        return Response(response, 200)

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

class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
