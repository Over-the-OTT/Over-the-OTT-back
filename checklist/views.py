import requests

from django.shortcuts import get_object_or_404

from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from checklist.models import MovieContent, TVContent

from overtheott.settings import TMDB_API_KEY
from .serializers import *

class MovieSearchView(views.APIView):    
    def get(self, request):
        api_key=TMDB_API_KEY
        keyword=request.GET.get('keyword', None)

        if not keyword:
            list_url="https://api.themoviedb.org/3/movie/popular?api_key="+api_key+"&language=ko-KR"
        else:
            list_url = "https://api.themoviedb.org/3/search/movie?api_key="+api_key+"&language=ko-KR&query="+keyword
        list_response = requests.get(list_url).json()['results']
        
        data = []    

        for l in list_response:
            tmdb_id = str(l['id'])
            detail_url = "https://api.themoviedb.org/3/movie/"+tmdb_id+"?api_key="+api_key+"&language=ko-KR"
            detail_response = requests.get(detail_url).json()
            
            provider_url = "https://api.themoviedb.org/3/movie/"+tmdb_id+"/watch/providers?api_key="+api_key
            
            try:
                provider_response = requests.get(provider_url).json()['results']['KR']['flatrate']
                provider_list = []
                for p in provider_response:
                    provider_list.append(p['provider_name'])
            except KeyError:  
                continue

            result = {}
            result['tmdb_id']=detail_response['id']
            result['title'] = detail_response['title']
            result['poster'] = detail_response['backdrop_path']
            result['runtime'] = detail_response['runtime']
            result['provider'] = provider_list
            data.append(result)
            
        return Response({'message': '영화 목록 조회 성공', 'data': data}, status=HTTP_200_OK)
    
    def post(self, request):
        movie_data = {
            'user': 1,
            'title': request.data.get('title'),
            'tmdb_id': request.data.get('tmdb_id'),
            'poster': request.data.get('poster'),
            'provider': request.data.get('provider'),
            'runtime': request.data.get('runtime')
        }

        serializer = MovieSerializer(data=movie_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '영화 저장 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '영화 저장 실패'}, serializer.errors, status=HTTP_400_BAD_REQUEST)


class TVSearchView(views.APIView):
    def get(self, request):
        api_key=TMDB_API_KEY
        keyword=request.GET.get('keyword')

        if not keyword:
            list_url="https://api.themoviedb.org/3/tv/popular?api_key="+api_key+"&language=ko-KR"
        else:
            list_url = "https://api.themoviedb.org/3/search/tv?api_key="+api_key+"&language=ko-KR&query="+keyword
        list_response = requests.get(list_url).json()['results']
        
        data = []    

        for l in list_response:
            tmdb_id = str(l['id'])
            detail_url = "https://api.themoviedb.org/3/tv/"+tmdb_id+"?api_key="+api_key+"&language=ko-KR"
            detail_response = requests.get(detail_url).json()

            provider_url = "https://api.themoviedb.org/3/tv/"+tmdb_id+"/watch/providers?api_key="+api_key
            
            try:
                provider_response = requests.get(provider_url).json()['results']['KR']['flatrate']
                provider_list = []
                for p in provider_response:
                    provider_list.append(p['provider_name'])
            except KeyError:  
                continue
            
            season=[]

            for e in range(1,len(detail_response['seasons'])+1):
                season_detail={}

                season_url = "https://api.themoviedb.org/3/tv/"+tmdb_id+"/season/"+str(e)+"?api_key="+api_key
                season_detail['season']=e

                try:
                    season_detail['episodes']=len(requests.get(season_url).json()['episodes'])
                except KeyError:
                    season_detail['episodes']=None

                season.append(season_detail)

            result = {}

            result['tmdb_id']=detail_response['id']
            result['title'] = detail_response['name']
            result['poster'] = detail_response['backdrop_path']
            result['episode_run_time'] = detail_response['episode_run_time'][0]
            result['season']=season
            result['provider'] = provider_list

            data.append(result)

        return Response({'message': 'TV 목록 조회 성공', 'data': data}, status=HTTP_200_OK)
    
    def post(self, request):
        tv_data = {
            'user': 1,
            'title': request.data.get('title'),
            'tmdb_id': request.data.get('tmdb_id'),
            'poster': request.data.get('poster'),
            'season': request.data.get('season'),
            'episode': request.data.get('episode'),
            'provider': request.data.get('provider'),
            'runtime': request.data.get('episode_run_time')
        }

        serializer = TVSerializer(data=tv_data)

        if serializer.is_valid():
            serializer.save()
            
            tv_id = serializer.data['id']  

            for i in range(serializer.data['episode']):
                episode_data = {'tv': tv_id, 'episode_num': i+1}
                episode_serializer = EpisodeSerializer(data=episode_data)

                if episode_serializer.is_valid():
                    episode_serializer.save()


            return Response({'message': '드라마 저장 성공', 'data': serializer.data}, status=HTTP_200_OK)
        else:
            return Response({'message': '드라마 저장 실패'}, serializer.errors, status=HTTP_400_BAD_REQUEST)


class MovieListView(views.APIView):
    def get(self, request):
        watching_movies = MovieContent.objects.filter(is_finished=False)
        watched_movies = MovieContent.objects.filter(is_finished=True)
        
        watching_movie_serializer = MovieListSerializer(watching_movies, many=True)
        watched_movie_serializer = MovieListSerializer(watched_movies, many=True)

        return Response({'message': '체크리스트 조회 성공', 'data': {'watching': watching_movie_serializer.data, 'watched': watched_movie_serializer.data}}, status=HTTP_200_OK)


class MovieDetailView(views.APIView):
    def get(self, request, pk):
        movie = get_object_or_404(MovieContent, pk=pk)
        movie_serializer = MovieSerializer(movie)

        return Response({'message': '체크리스트 조회 성공', 'data': movie_serializer.data}, status=HTTP_200_OK)


class TVListView(views.APIView):
    def get(self, request):
        watching_tv = TVContent.objects.filter(is_finished=False)
        watched_tv = TVContent.objects.filter(is_finished=True)
        
        watching_tv_serializer = MovieListSerializer(watching_tv, many=True)
        watched_tv_serializer = MovieListSerializer(watched_tv, many=True)

        return Response({'message': '체크리스트 조회 성공', 'data': {'watching': watching_tv_serializer.data, 'watched': watched_tv_serializer.data}}, status=HTTP_200_OK)


class TVDetailView(views.APIView):
    def get(self, request, pk):
        tv = get_object_or_404(TVContent, pk=pk)
        tv_seriallizer = TVDetailSerializer(tv)

        return Response({'message': '드라마 상세 조회 성공', 'data': tv_seriallizer.data}, status=HTTP_200_OK)

