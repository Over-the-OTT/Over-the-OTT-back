from .serializers import *
from .models import *
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.status import *
# Create your views here.


class RuntimeView(views.APIView):
    def get(self, request):
        runtime = Runtime.objects.filter(ott__user=request.user)
        serializer = RuntimeSerializer(runtime, many=True)
        return Response({'message': '런타임 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

class DaysTillView(views.APIView):
    def get(self, request):
        days_till = SubscribingOTT.objects.filter(user=request.user)
        serializer = DaysTillSerializer(days_till, many=True)
        return Response({'message': '남은 결제일 조회 성공', 'data': serializer.data}, status=HTTP_200_OK)

