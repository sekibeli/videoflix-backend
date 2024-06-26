from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.db.models import Count, Q

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import VideoSerializer, VideoQualitySerializer
from .models import Video, VideoQuality
from datetime import datetime, timedelta

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoSearchView(APIView):
    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search', None)
        if search is not None:
            videos = Video.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search),
                isVisible=True
            )
        else:
            videos = Video.objects.filter(isVisible=True)

        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        cache_key = 'video_list_cache_key'
        video_list = cache.get(cache_key)

        if not video_list:
            response = super(VideoViewSet, self).list(request, *args, **kwargs)
            video_list = response.data
            cache.set(cache_key, video_list, timeout=CACHE_TTL)
            from_cache = False
        else:
            from_cache = True

        response = Response(video_list)
        if from_cache:
            response['X-Cache'] = 'HIT'
        else:
            response['X-Cache'] = 'MISS'
        return response

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            queryset = Video.objects.filter(isVisible=True)
            category = self.request.query_params.get('category', None)
            if category is not None:
                queryset = queryset.filter(category=category)
            return queryset

    def perform_create(self, serializer):
        serializer.save(created_from=self.request.user)
        cache.delete('video_list_cache_key')

    def retrieve(self, request, *args, **kwargs):
        video = get_object_or_404(Video, pk=kwargs['pk'])
        qualities = VideoQuality.objects.filter(video=video)
        video_data = VideoSerializer(video, context={'request': request}).data
        quality_data = VideoQualitySerializer(qualities, many=True, context={'request': request}).data
        video_data['qualities'] = quality_data
        return Response(video_data)

    def perform_update(self, serializer):
        serializer.save(created_from=self.request.user)
        cache.delete('video_list_cache_key')

    @action(detail=False, methods=['get'])
    def videos_today(self, request):
        cache_key = 'videos_today_cache_key'
        videos_today = cache.get(cache_key)

        if not videos_today:
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            queryset = Video.objects.filter(created_at__gte=today, created_at__lt=tomorrow, isVisible=True)
            serializer = VideoSerializer(queryset, many=True, context={'request': request})
            videos_today = serializer.data
            cache.set(cache_key, videos_today, timeout=CACHE_TTL)
            from_cache = False
        else:
            from_cache = True

        response = Response(videos_today)
        if from_cache:
            response['X-Cache'] = 'HIT'
        else:
            response['X-Cache'] = 'MISS'
        return response

    @action(detail=False, methods=['get'])
    def videos_yesterday(self, request):
        cache_key = 'videos_yesterday_cache_key'
        videos_yesterday = cache.get(cache_key)

        if not videos_yesterday:
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
            queryset = Video.objects.filter(created_at__gte=yesterday, created_at__lt=today, isVisible=True)
            serializer = VideoSerializer(queryset, many=True, context={'request': request})
            videos_yesterday = serializer.data
            cache.set(cache_key, videos_yesterday, timeout=CACHE_TTL)
            from_cache = False
        else:
            from_cache = True

        response = Response(videos_yesterday)
        if from_cache:
            response['X-Cache'] = 'HIT'
        else:
            response['X-Cache'] = 'MISS'
        return response

    @action(detail=False, methods=['get'])
    def recentVideos(self, request):
        cache_key = 'recent_videos_cache_key'
        recent_videos = cache.get(cache_key)

        if not recent_videos:
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            three_days_ago = today - timedelta(days=3)
            queryset = Video.objects.filter(created_at__gte=three_days_ago, created_at__lt=tomorrow, isVisible=True)
            serializer = VideoSerializer(queryset, many=True, context={'request': request})
            recent_videos = serializer.data
            cache.set(cache_key, recent_videos, timeout=CACHE_TTL)
            from_cache = False
        else:
            from_cache = True

        response = Response(recent_videos)
        if from_cache:
            response['X-Cache'] = 'HIT'
        else:
            response['X-Cache'] = 'MISS'
        return response

    @action(detail=False, methods=['get'])
    def popular_videos(self, request):
        cache_key = 'popular_videos_cache_key'
        popular_videos = cache.get(cache_key)

        if not popular_videos:
            videos_with_like_count = Video.objects.filter(isVisible=True).annotate(likes_count=Count('likes')).order_by('-likes_count')[:10]
            serializer = VideoSerializer(videos_with_like_count, many=True, context={'request': request})
            popular_videos = serializer.data
            cache.set(cache_key, popular_videos, timeout=CACHE_TTL)
            from_cache = False
        else:
            from_cache = True

        response = Response(popular_videos)
        if from_cache:
            response['X-Cache'] = 'HIT'
        else:
            response['X-Cache'] = 'MISS'
        return response

    @action(detail=False, methods=['get'])
    def mostSeen_videos(self, request):
        cache_key = 'most_seen_videos_cache_key'
        most_seen_videos = cache.get(cache_key)

        if not most_seen_videos:
            videos_seen = Video.objects.filter(isVisible=True).annotate(views_count=Count('view_count')).order_by('-view_count')[:10]
            serializer = VideoSerializer(videos_seen, many=True, context={'request': request})
            most_seen_videos = serializer.data
            cache.set(cache_key, most_seen_videos, timeout=CACHE_TTL)
            from_cache = False
        else:
            from_cache = True

        response = Response(most_seen_videos)
        if from_cache:
            response['X-Cache'] = 'HIT'
        else:
            response['X-Cache'] = 'MISS'
        return response

    @action(detail=True, methods=['post'])
    def increment_view_count(self, request, pk=None):
        video = self.get_object()
        video.view_count += 1
        video.save()
        cache.delete('video_list_cache_key')
        return Response({'status': 'view count incremented'})
