from django.shortcuts import get_object_or_404, render
from .serializers import *
from .models import *
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.status import *
from django.contrib.auth import logout, login

# Create your views here.


class SignUpView(views.APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(
            context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data})
        return Response({'message': '회원가입 실패', 'error': serializer.errors})

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'message': '유저 목록 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

    def patch(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'username 입력 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': 'username 입력 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({'message': "로그인 성공", 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': "로그인 실패", 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    def get(self, request, format=None):
        logout(request)
        return Response({'message': "로그아웃 성공"}, status=HTTP_200_OK)


class SubscribingOTTView(views.APIView):
    def post(self, request):
        serializer = SubscribingOTTSerializer(
            data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '구독 중인 OTT 생성 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '구독 중인 OTT 생성 실패', 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def get(self, request):
        otts = SubscribingOTT.objects.filter(user=request.user)
        serializer = SubscribingOTTSerializer(otts, many=True)
        return Response({'message': '구독 중인 OTT 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

    def put(self, request):
        data = request.data
        instances = []
        for ott in data:
            obj = get_object_or_404(SubscribingOTT, id=ott['id'])
            obj.id = ott['id']
            obj.user = request.user
            obj.fee = ott['fee']
            obj.pay_date = ott['pay_date']
            obj.share = ott['share']
            obj.save()
            instances.append(obj)
        serializer = OTTDetailSerializer(
            instances, many=True, partial=True)
        return Response({'messsage': '상세 구독 정보 입력 성공', 'data': serializer.data}, status=HTTP_200_OK)


class SubsOTTDetailView(views.APIView):
    def put(self, request, pk):
        ott = get_object_or_404(SubscribingOTT, pk=pk)
        serializer = OTTDetailSerializer(ott, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '구독 중인 ott 수정 성공', 'data': serializer.data}, status=HTTP_200_OK)
        return Response({'message': '구독 중인 ott 수정 실패', 'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ott = get_object_or_404(SubscribingOTT, pk=pk)
        ott.delete()
        return Response({'message': '구독 중인 ott 삭제 성공'}, status=HTTP_200_OK)
