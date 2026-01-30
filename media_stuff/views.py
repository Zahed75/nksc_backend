from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone

from .models import GalleryCategory, GalleryEvent, GalleryImage, GalleryVideo
from .serializers import (
    GalleryCategorySerializer,
    GalleryEventSerializer,
    GalleryEventListSerializer,
    GalleryImageSerializer,
    GalleryVideoSerializer
)


# ========== PUBLIC API ENDPOINTS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_gallery_events(request):
    """
    Get all published gallery events
    Query Parameters:
    - category: Filter by category slug
    - year: Filter by year
    - featured: true/false
    - search: Search term
    - limit: Results limit (default: 20)
    """
    category_slug = request.query_params.get('category', None)
    year = request.query_params.get('year', None)
    featured = request.query_params.get('featured', None)
    search = request.query_params.get('search', None)
    limit = int(request.query_params.get('limit', 20))

    # Get published events
    events = GalleryEvent.objects.filter(status='published')

    # Apply filters
    if category_slug:
        events = events.filter(category__slug=category_slug)

    if year:
        try:
            year_int = int(year)
            events = events.filter(event_date__year=year_int)
        except ValueError:
            pass

    if featured and featured.lower() == 'true':
        events = events.filter(is_featured=True)

    if search:
        events = events.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(short_description__icontains=search) |
            Q(location__icontains=search)
        )

    # Order results
    events = events.order_by('-event_date', '-created_at')

    # Apply limit
    events = events[:limit]

    serializer = GalleryEventListSerializer(events, many=True, context={'request': request})

    return Response({
        'success': True,
        'count': events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_event_by_slug(request, slug):
    """Get detailed gallery event by slug"""
    event = get_object_or_404(GalleryEvent, slug=slug, status='published')

    # Increment view count
    event.increment_views()

    serializer = GalleryEventSerializer(event, context={'request': request})

    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_event_images(request, slug):
    """Get all images for a gallery event"""
    event = get_object_or_404(GalleryEvent, slug=slug, status='published')
    images = event.images.all().order_by('display_order')

    serializer = GalleryImageSerializer(images, many=True, context={'request': request})

    return Response({
        'success': True,
        'event_title': event.title,
        'count': images.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_event_videos(request, slug):
    """Get all videos for a gallery event"""
    event = get_object_or_404(GalleryEvent, slug=slug, status='published')
    videos = event.videos.all().order_by('display_order')

    serializer = GalleryVideoSerializer(videos, many=True, context={'request': request})

    return Response({
        'success': True,
        'event_title': event.title,
        'count': videos.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_categories(request):
    """Get all gallery categories"""
    categories = GalleryCategory.objects.all().order_by('display_order')

    categories_data = []
    for category in categories:
        event_count = category.events.filter(status='published').count()
        category_data = GalleryCategorySerializer(category).data
        category_data['event_count'] = event_count
        categories_data.append(category_data)

    return Response({
        'success': True,
        'count': len(categories_data),
        'data': categories_data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_years(request):
    """Get distinct years from gallery events"""
    years = GalleryEvent.objects.filter(
        status='published'
    ).dates('event_date', 'year').order_by('-event_date')

    years_list = [{'value': year.year, 'label': str(year.year)} for year in years]

    return Response({
        'success': True,
        'count': len(years_list),
        'data': years_list
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_stats(request):
    """Get gallery statistics"""
    total_events = GalleryEvent.objects.filter(status='published').count()
    total_images = GalleryImage.objects.count()
    total_videos = GalleryVideo.objects.count()
    total_views = GalleryEvent.objects.filter(status='published').aggregate(
        total=Count('views_count')
    )['total'] or 0

    return Response({
        'success': True,
        'stats': {
            'total_events': total_events,
            'total_images': total_images,
            'total_videos': total_videos,
            'total_views': total_views,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_photo_galleries(request):
    """Get only photo galleries (events with images)"""
    events = GalleryEvent.objects.filter(
        status='published',
        images__isnull=False
    ).distinct().order_by('-event_date')[:12]

    serializer = GalleryEventListSerializer(events, many=True, context={'request': request})

    return Response({
        'success': True,
        'count': events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_galleries(request):
    """Get only video galleries (events with videos)"""
    events = GalleryEvent.objects.filter(
        status='published',
        videos__isnull=False
    ).distinct().order_by('-event_date')[:12]

    serializer = GalleryEventListSerializer(events, many=True, context={'request': request})

    return Response({
        'success': True,
        'count': events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def search_gallery_events(request):
    """Search gallery events"""
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', None)
    year = request.query_params.get('year', None)

    events = GalleryEvent.objects.filter(status='published')

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(location__icontains=query)
        )

    if category:
        events = events.filter(category__slug=category)

    if year:
        try:
            year_int = int(year)
            events = events.filter(event_date__year=year_int)
        except ValueError:
            pass

    events = events.order_by('-event_date')[:50]

    serializer = GalleryEventListSerializer(events, many=True, context={'request': request})

    return Response({
        'success': True,
        'query': query,
        'count': events.count(),
        'data': serializer.data
    })