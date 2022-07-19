from rest_framework import serializers
from .models import *


class OTTSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTT
        fields = ['name', 'fee']


class SubsOTTSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribingOTT
        fields = ['id', 'user', 'ott', 'start_date']


class ToWatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToWatchContent
        fields = ['id', 'user', 'content_id', 'ott', 'added_at']


class WatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedContent
        fields = ['id', 'user', 'content_id', 'ott', 'added_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'], username=validated_data['username'],)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):  # 유효성 검사가 끝나지 않은 데이터니까 validated_data가 아닌 그냥 data를 가져옴
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
