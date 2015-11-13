from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, validated_data):
        password = validated_data.get('password', User.objects.make_random_password())
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=password
        )
        user.set_password(password)
        user.save()
        return user