from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError()
            else:
                return user
        else:
            raise serializers.ValidationError()


class SubscribingOTTSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribingOTT
        fields = ['id', 'user', 'ott']


class OTTDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribingOTT
        fields = ['id', 'user', 'ott', 'fee', 'pay_date', 'share']
