from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieContent
        fields = ['id', 'user', 'title', 'tmdb_id', 'poster', 'provider', 'runtime', 'added_at', 'is_finished']


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieContent
        fields = ['id', 'title', 'provider', 'is_finished']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'tv', 'episode_num', 'is_finished']


class TVSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVContent
        fields = ['id', 'user', 'title', 'tmdb_id', 'poster', 'provider', 'runtime', 'season', 'episode', 'added_at', 'is_finished']


class TVListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVContent
        fields = ['id', 'title', 'season', 'provider', 'is_finished']


class TVDetailSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = TVContent
        fields = ['id', 'user', 'title', 'tmdb_id', 'poster', 'provider', 'runtime', 'season', 'episode', 'episodes', 'added_at', 'is_finished']