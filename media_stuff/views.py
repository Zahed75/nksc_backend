from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone
from django.http import JsonResponse

from .models import GalleryCategory, GalleryEvent, GalleryImage, GalleryStat
from .serializers import (
    GalleryCategorySerializer, 
    GalleryEventSerializer,
    GalleryEventListSerializer,
    GalleryImageSerializer
)


# ========== HELPER FUNCTIONS ==========

def get_or_create_stats():
    """Get or create gallery statistics"""
    stats, created = GalleryStat.objects.get_or_create(
        defaults={
            'total_events': GalleryEvent.objects.filter(status='published').count(),
            'total_images': GalleryImage.objects.count(),
            'total_views': GalleryEvent.objects.filter(status='published').aggregate(
                total=Count('views_count')
            )['total'] or 0,
            'seminar_count': GalleryEvent.objects.filter(
                status='published', 
                category__name='seminar'
            ).count(),
            'workshop_count': GalleryEvent.objects.filter(
                status='published', 
                category__name='workshop'
            ).count(),
            'conference_count': GalleryEvent.objects.filter(
                status='published', 
                category__name='conference'
            ).count(),
            'cultural_count': GalleryEvent.objects.filter(
                status='published', 
                category__name='cultural'
            ).count(),
        }
    )
    return stats


# ========== PUBLIC API ENDPOINTS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_gallery_events(request):
    """
    Get all published gallery events with filtering options
    Query Parameters:
    - category: Filter by category slug
    - year: Filter by year
    - featured: Filter featured events (true/false)
    - search: Search in title, description, location
    - limit: Limit results (default: 20)
    - page: Page number
    """
    # Get query parameters
    category_slug = request.query_params.get('category', None)
    year = request.query_params.get('year', None)
    featured = request.query_params.get('featured', None)
    search = request.query_params.get('search', None)
    limit = int(request.query_params.get('limit', 20))
    
    # Start with published events
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
            Q(location__icontains=search) |
            Q(organizer__icontains=search)
        )
    
    # Order by featured first, then event date
    events = events.order_by('-is_featured', '-event_date', '-created_at')
    
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
def get_featured_gallery_events(request):
    """Get featured gallery events (limit: 6)"""
    featured_events = GalleryEvent.objects.filter(
        status='published',
        is_featured=True
    ).order_by('-event_date', '-created_at')[:6]
    
    serializer = GalleryEventListSerializer(featured_events, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': featured_events.count(),
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
    """Get all images for a specific gallery event"""
    event = get_object_or_404(GalleryEvent, slug=slug, status='published')
    images = event.images.all().order_by('display_order', 'created_at')
    
    serializer = GalleryImageSerializer(images, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'event_title': event.title,
        'event_slug': event.slug,
        'count': images.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_categories(request):
    """Get all gallery categories with event counts"""
    categories = GalleryCategory.objects.all()
    
    # Annotate with event count
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
    stats = get_or_create_stats()
    
    # Update stats
    stats.total_events = GalleryEvent.objects.filter(status='published').count()
    stats.total_images = GalleryImage.objects.count()
    stats.total_views = GalleryEvent.objects.filter(status='published').aggregate(
        total=Count('views_count')
    )['total'] or 0
    
    # Update category counts
    stats.seminar_count = GalleryEvent.objects.filter(
        status='published', 
        category__name='seminar'
    ).count()
    stats.workshop_count = GalleryEvent.objects.filter(
        status='published', 
        category__name='workshop'
    ).count()
    stats.conference_count = GalleryEvent.objects.filter(
        status='published', 
        category__name='conference'
    ).count()
    stats.cultural_count = GalleryEvent.objects.filter(
        status='published', 
        category__name='cultural'
    ).count()
    
    stats.save()
    
    return Response({
        'success': True,
        'stats': {
            'total_events': stats.total_events,
            'total_images': stats.total_images,
            'total_views': stats.total_views,
            'seminar_count': stats.seminar_count,
            'workshop_count': stats.workshop_count,
            'conference_count': stats.conference_count,
            'cultural_count': stats.cultural_count,
            'other_count': stats.total_events - (
                stats.seminar_count + stats.workshop_count + 
                stats.conference_count + stats.cultural_count
            ),
            'last_updated': stats.last_updated
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gallery_by_category(request, category_slug):
    """Get gallery events by category slug"""
    category = get_object_or_404(GalleryCategory, slug=category_slug)
    events = GalleryEvent.objects.filter(
        status='published',
        category=category
    ).order_by('-event_date', '-created_at')
    
    serializer = GalleryEventListSerializer(events, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'category': GalleryCategorySerializer(category).data,
        'count': events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_latest_gallery_events(request):
    """Get latest gallery events (limit: 12)"""
    latest_events = GalleryEvent.objects.filter(
        status='published'
    ).order_by('-event_date', '-created_at')[:12]
    
    serializer = GalleryEventListSerializer(latest_events, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': latest_events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def search_gallery_events(request):
    """Search gallery events with advanced filtering"""
    query = request.query_params.get('q', '')
    category = request.query_params.get('category', None)
    year = request.query_params.get('year', None)
    location = request.query_params.get('location', None)
    
    events = GalleryEvent.objects.filter(status='published')
    
    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(location__icontains=query) |
            Q(organizer__icontains=query)
        )
    
    if category:
        events = events.filter(category__slug=category)
    
    if year:
        try:
            year_int = int(year)
            events = events.filter(event_date__year=year_int)
        except ValueError:
            pass
    
    if location:
        events = events.filter(location__icontains=location)
    
    events = events.order_by('-event_date', '-created_at')[:50]
    
    serializer = GalleryEventListSerializer(events, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'query': query,
        'filters': {
            'category': category,
            'year': year,
            'location': location
        },
        'count': events.count(),
        'data': serializer.data
    })