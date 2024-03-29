from rest_framework import serializers
from .models import *


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieContent
        fields = ['id', 'user', 'title', 'tmdb_id', 'poster',
                  'provider', 'runtime', 'added_at', 'is_finished']


class MovieListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = MovieContent
        fields = ['id', 'type', 'title', 'provider', 'is_finished']

    def get_type(self, obj):
        return 'movie'


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'tv', 'episode_num', 'is_finished']


class TVSerializer(serializers.ModelSerializer):
    class Meta:
        model = TVContent
        fields = ['id', 'user', 'title', 'tmdb_id', 'poster', 'provider', 'runtime',
                  'season', 'total_episode', 'episode_status', 'added_at', 'is_finished']


class TVListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = TVContent
        fields = ['id', 'type', 'title', 'season', 'provider', 'is_finished']

    def get_type(self, obj):
        return 'tv'


class TVDetailSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = TVContent
        fields = ['id', 'user', 'title', 'tmdb_id', 'poster', 'provider', 'runtime',
                  'season', 'total_episode', 'episode_status', 'episodes', 'added_at', 'is_finished']
