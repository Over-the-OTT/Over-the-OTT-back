import requests

from django.shortcuts import get_object_or_404
from datetime import datetime

from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from account.models import SubscribingOTT
from checklist.models import MovieContent, TVContent
from calculator.models import Runtime

from overtheott.settings import TMDB_API_KEY
from .serializers import *


class MovieSearchView(views.APIView):
    def get(self, request):
        api_key = TMDB_API_KEY
        keyword = request.GET.get('keyword', None)

        if not keyword:
            list_url = "https://api.themoviedb.org/3/movie/popular?api_key=" + \
                api_key+"&language=ko-KR"
        else:
            list_url = "https://api.themoviedb.org/3/search/movie?api_key=" + \
                api_key+"&language=ko-KR&query="+keyword
        list_response = requests.get(list_url).json()['results']

        data = []

        for l in list_response:
            tmdb_id = str(l['id'])
            detail_url = "https://api.themoviedb.org/3/movie/" + \
                tmdb_id+"?api_key="+api_key+"&language=ko-KR"
            detail_response = requests.get(detail_url).json()

            provider_url = "https://api.themoviedb.org/3/movie/" + \
                tmdb_id+"/watch/providers?api_key="+api_key

            try:
                provider_response = requests.get(provider_url).json()[
                    'results']['KR']['flatrate']
                provider_list = []
                for p in provider_response:
                    provider_list.append(p['provider_name'])
            except KeyError:
                continue

            result = {}
            result['tmdb_id'] = detail_response['id']
            result['title'] = detail_response['title']
            result['poster'] = detail_response['backdrop_path']
            result['runtime'] = detail_response['runtime']
            result['provider'] = provider_list
            data.append(result)

        return Response({'message': '영화 목록 검색 성공', 'data': data}, status=HTTP_200_OK)

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
            return Response({'message': '영화 저장 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class TVSearchView(views.APIView):
    def get(self, request):
        api_key = TMDB_API_KEY
        keyword = request.GET.get('keyword')

        if not keyword:
            list_url = "https://api.themoviedb.org/3/tv/popular?api_key="+api_key+"&language=ko-KR"
        else:
            list_url = "https://api.themoviedb.org/3/search/tv?api_key=" + \
                api_key+"&language=ko-KR&query="+keyword
        list_response = requests.get(list_url).json()['results']

        data = []

        for l in list_response:
            tmdb_id = str(l['id'])
            detail_url = "https://api.themoviedb.org/3/tv/" + \
                tmdb_id+"?api_key="+api_key+"&language=ko-KR"
            detail_response = requests.get(detail_url).json()

            provider_url = "https://api.themoviedb.org/3/tv/" + \
                tmdb_id+"/watch/providers?api_key="+api_key

            try:
                provider_response = requests.get(provider_url).json()[
                    'results']['KR']['flatrate']
                provider_list = []
                for p in provider_response:
                    provider_list.append(p['provider_name'])
            except KeyError:
                continue

            season = []

            for e in range(1, len(detail_response['seasons'])+1):
                season_detail = {}

                season_url = "https://api.themoviedb.org/3/tv/" + \
                    tmdb_id+"/season/"+str(e)+"?api_key="+api_key
                season_detail['season'] = e

                try:
                    season_detail['episodes'] = len(
                        requests.get(season_url).json()['episodes'])
                except KeyError:
                    season_detail['episodes'] = None

                season.append(season_detail)

            result = {}

            result['tmdb_id'] = detail_response['id']
            result['title'] = detail_response['name']
            result['poster'] = detail_response['backdrop_path']
            if detail_response['episode_run_time']:
                result['episode_run_time'] = detail_response['episode_run_time'][0]
            else:
                result['episode_run_time'] = 0
            result['season'] = season
            result['provider'] = provider_list

            data.append(result)

        return Response({'message': 'TV 목록 검색 성공', 'data': data}, status=HTTP_200_OK)

    def post(self, request):
        tv_data = {
            'user': 1,
            'title': request.data.get('title'),
            'tmdb_id': request.data.get('tmdb_id'),
            'poster': request.data.get('poster'),
            'season': request.data.get('season'),
            'total_episode': request.data.get('total_episode'),
            'provider': request.data.get('provider'),
            'runtime': request.data.get('episode_run_time')
        }

        serializer = TVSerializer(data=tv_data)

        if serializer.is_valid():
            serializer.save()

            tv_id = serializer.data['id']

            for i in range(serializer.data['total_episode']):
                episode_data = {'tv': tv_id, 'episode_num': i+1}
                episode_serializer = EpisodeSerializer(data=episode_data)

                if episode_serializer.is_valid():
                    episode_serializer.save()

            return Response({'message': 'TV 저장 성공', 'data': serializer.data}, status=HTTP_200_OK)

        else:
            return Response({'message': 'TV 저장 실패', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class MovieListView(views.APIView):
    def get(self, request):
        watching_movies = MovieContent.objects.filter(is_finished=False)
        watched_movies = MovieContent.objects.filter(is_finished=True)

        watching_movie_serializer = MovieListSerializer(
            watching_movies, many=True)
        watched_movie_serializer = MovieListSerializer(
            watched_movies, many=True)

        return Response({'message': '영화 체크리스트 조회 성공', 'data': {'watching': watching_movie_serializer.data, 'watched': watched_movie_serializer.data}}, status=HTTP_200_OK)


class MovieDetailView(views.APIView):
    def get(self, request, pk):
        movie = get_object_or_404(MovieContent, pk=pk)
        movie_serializer = MovieSerializer(movie)

        return Response({'message': '영화 체크리스트 상세 조회 성공', 'data': movie_serializer.data}, status=HTTP_200_OK)

    def post(self, request, pk):
        movie = get_object_or_404(MovieContent, pk=pk)
        subsott = get_object_or_404(SubscribingOTT.objects.filter(
            user=request.user.id, ott__ott=movie.provider))
        cur_year = datetime.now().year
        cur_month = datetime.now().month
        runtime, created = Runtime.objects.get_or_create(
            ott=subsott, year=cur_year, month=cur_month, defaults={'year': cur_year, 'month': cur_month})

        if movie.is_finished:
            movie.is_finished = False
            runtime.total_runtime -= movie.runtime
        else:
            movie.is_finished = True
            runtime.total_runtime += movie.runtime
        runtime.save()
        movie_serializer = MovieSerializer(movie)
        movie.save()
        return Response({'message': '영화 시청 기록 저장 성공', 'data': movie_serializer.data}, status=HTTP_200_OK)

    def delete(self, request, pk):
        movie = get_object_or_404(MovieContent, pk=pk)
        runtime = get_object_or_404(Runtime.objects.filter(
            ott__user=request.user.id, ott__ott__ott=movie.provider))

        runtime.total_runtime -= movie.runtime
        runtime.save()
        movie.delete()
        return Response({'message': '영화 컨텐츠 삭제 성공'}, status=HTTP_200_OK)


class TVListView(views.APIView):
    def get(self, request):
        watching_tv = TVContent.objects.filter(is_finished=False)
        watched_tv = TVContent.objects.filter(is_finished=True)

        watching_tv_serializer = MovieListSerializer(watching_tv, many=True)
        watched_tv_serializer = MovieListSerializer(watched_tv, many=True)

        return Response({'message': 'TV 체크리스트 조회 성공', 'data': {'watching': watching_tv_serializer.data, 'watched': watched_tv_serializer.data}}, status=HTTP_200_OK)


class TVDetailView(views.APIView):
    def get(self, request, pk):
        tv = get_object_or_404(TVContent, pk=pk)
        tv_seriallizer = TVDetailSerializer(tv)

        return Response({'message': 'TV 체크리스트 상세 조회 성공', 'data': tv_seriallizer.data}, status=HTTP_200_OK)

    def post(self, request, pk):
        episode_id = request.data.get('episode_id')
        episode = get_object_or_404(Episode, pk=episode_id)
        subsott = get_object_or_404(SubscribingOTT.objects.filter(
            user=request.user.id, ott__ott=episode.tv.provider))
        cur_year = datetime.now().year
        cur_month = datetime.now().month
        runtime, created = Runtime.objects.get_or_create(
            ott=subsott, year=cur_year, month=cur_month, defaults={'year': cur_year, 'month': cur_month})
        tv = episode.tv

        if episode.is_finished:
            episode.is_finished = False
            tv.episode_status -= 1
            runtime.total_runtime -= tv.runtime
        else:
            episode.is_finished = True
            tv.episode_status += 1
            runtime.total_runtime += tv.runtime
        runtime.save()
        episode_serializer = EpisodeSerializer(episode)
        episode.save()

        if tv.total_episode == tv.episode_status:
            tv.is_finished = True
        else:
            tv.is_finished = False
        tv.save()

        return Response({'message': 'TV 시청 기록 저장 성공', 'data': episode_serializer.data}, status=HTTP_200_OK)

    def put(self, request, pk):
        tv = get_object_or_404(TVContent, pk=pk)
        episodes = tv.episodes.all()
        runtime = get_object_or_404(Runtime.objects.filter(
            ott__user=1, ott__ott__ott=tv.provider))  # ott__user=request.user.id

        for ep in episodes:
            ep.is_finished = True
            ep.save()
        tv.episode_status = tv.total_episode
        tv.is_finished = True
        runtime.total_runtime += tv.runtime * tv.total_episode
        tv_serializer = TVDetailSerializer(tv)
        tv.save()
        runtime.save()

        return Response({'message': 'TV 에피소드 전체 토글 성공', 'data': tv_serializer.data}, status=HTTP_200_OK)

    def delete(self, request, pk):
        tv = get_object_or_404(TVContent, pk=pk)
        runtime = get_object_or_404(Runtime.objects.filter(
            ott__user=1, ott__ott__ott=tv.provider))  # ott__user=request.user.id

        runtime.total_runtime -= tv.runtime * tv.episode_status
        runtime.save()
        tv.delete()
        return Response({'message': 'TV 컨텐츠 삭제 성공'}, status=HTTP_200_OK)
