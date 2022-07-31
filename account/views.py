from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import *
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

# Create your views here.


class SignUpView(views.APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data})
        return Response({'message': '회원가입 실패', 'error': serializer.errors})


class LoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.data})
        return Response({'message': "로그인 실패", 'data': serializer.errors})


class LogoutView(views.APIView):
    def get(self, request, format=None):
        logout(request)
        return Response({'message': "로그아웃 성공"})


class SubscribingOTTView(views.APIView):

    def post(self, request):
        data = request.data
        serializer = SubscribingOTTSerializer(
            data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '구독 중인 OTT 생성 성공', 'data': serializer.data})
        return Response({'message': '구독 중인 OTT 생성 실패', 'error': serializer.errors})

    def get(self, request):
        otts = SubscribingOTT.objects.filter(user=request.user)
        serializer = SubscribingOTTSerializer(otts, many=True)
        return Response(serializer.data)

    def put(self, request):
        data = request.data
        instances = []
        for ott in data:
            obj = get_object_or_404(SubscribingOTT, id=ott['id'])
            obj.id = ott['id']
            obj.user = request.user
            obj.fee = ott['fee']
            obj.start_date = ott['start_date']
            obj.share = ott['share']
            obj.save()
            instances.append(obj)
        serializer = OTTDetailSerializer(
            instances, many=True, partial=True)
        return Response(serializer.data)
