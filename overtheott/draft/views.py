from django.shortcuts import get_object_or_404, render
import requests
import json

from .serializers import *
from .models import *
from rest_framework import views
from rest_framework.response import Response


# Create your views here.

# my_id = config.tmdbapi


# def test(request, query):

#     url1 = "https://api.themoviedb.org/3/search/movie?api_key=" + my_id + "&language=en-US&query=" + \
#         query + "&page=1&include_adult=false"

#     response = requests.get(url1)
#     resdata = response.text

#     obj = json.loads(resdata)
#     obj = obj['results']

#     runtime_results = []
#     for o in obj:
#         id = str(o['id'])
#         url2 = "https://api.themoviedb.org/3/movie/" + id + \
#             "?api_key=" + my_id + "&language=en-US"
#         response2 = requests.get(url2)
#         resdata2 = response2.text
#         obj2 = json.loads(resdata2)

#         result = {}
#         result['title'] = obj2['original_title']
#         result['runtime'] = obj2['runtime']
#         runtime_results.append(result)

#     return render(request, 'index.html', {'obj': obj, 'obj2': runtime_results})


class OTTView(views.APIView):
    def get(self, request, format=None):
        otts = OTT.objects.all()
        serializer = OTTSerializer(otts, many=True)
        return Response({'message': '전체 OTT 목록 조회 성공', 'data': serializer.data})

    def post(self, request, format=None):
        serializer = OTTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        ott = get_object_or_404(OTT, pk=pk)
        ott.delete()
        return Response()


class SubsOTTView(views.APIView):
    def get(self, request, format=None):
        otts = SubscribingOTT.objects.all()
        serializer = SubsOTTSerializer(otts, many=True)
        return Response({'message': '구독중인 OTT 목록 조회 성공', 'data': serializer.data})

    def post(self, request, format=None):
        serializer = SubsOTTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def put(self, request, pk, format=None):
        ott = get_object_or_404(OTT, pk=pk)
        serializer = SubsOTTSerializer(ott, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        ott = get_object_or_404(OTT, pk=pk)
        ott.delete()
        return Response()


class ToWatchView(views.APIView):
    def get(self, request, format=None):
        contents = ToWatchContent.objects.all()
        serializer = ToWatchSerializer(contents, many=True)
        return Response({'message': '정주행할 컨텐츠 목록 조회 성공', 'data': serializer.data})

    def post(self, request, format=None):
        serializer = ToWatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '정주행할 컨텐츠 목록 추가 성공', 'data': serializer.data})
        return Response(serializer.errors)

    def put(self, request, pk, format=None):
        content = get_object_or_404(ToWatchContent, pk=pk)
        serializer = ToWatchContent(content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '정주행할 컨텐츠 목록 수정 성공', 'data': serializer.data})
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        ott = get_object_or_404(OTT, pk=pk)
        ott.delete()
        return Response({'message': '정주행할 OTT 삭제 성공'})


class SignUpView(views.APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공', 'data': serializer.data})
        return Response({'message': '회원가입 실패', 'error': serializer.errors})

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'message': '유저 목록 조회 성공', 'data': serializer.data})


class LoginView(views.APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response({'message': "로그인 성공", 'data': serializer.data})
        return Response({'message': "로그인 실패", 'data': serializer.errors})
