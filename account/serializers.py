from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],)
        user.set_password(validated_data['password'])
        user.save()

        return user
