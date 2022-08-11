from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import *
from django.contrib.auth import login


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'username']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        login(self.context['request'], user)
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


class OTTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTT
        fields = ['id', 'ott', 'membership', 'fee']


class SubscribingOTTSerializer(serializers.ModelSerializer):
    ott = OTTSerializer(read_only=True)
    ott_name = serializers.CharField(write_only=True)
    membership = serializers.CharField(write_only=True)

    class Meta:
        model = SubscribingOTT
        fields = ['id', 'user', 'ott', 'ott_name',
                  'membership', 'pay_date', 'pay_amount', 'share']

    def create(self, validated_data):
        ottname = validated_data.pop('ott_name')
        membership = validated_data.pop('membership')
        ott = get_object_or_404(OTT.objects.filter(
            ott=ottname, membership=membership))
        validated_data['ott'] = ott
        subott = SubscribingOTT.objects.create(**validated_data)
        subott.save()
        return subott


class OTTDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribingOTT
        fields = ['id', 'user', 'ott', 'pay_date', 'share']
