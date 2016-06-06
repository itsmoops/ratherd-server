from rest_framework import serializers
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def create(self, validated_data):
        password = validated_data.get('password', User.objects.make_random_password())
        if not validated_data.get('email'):
            raise serializers.ValidationError('Invalid email')
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError({
                'email': [
                    'This email address is already in use.'
                ]
            })
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=password
        )
        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username'
		)
		read_only_fields =('id')
