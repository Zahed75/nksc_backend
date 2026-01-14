from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import News, NewsCategory
from .serializers import NewsSerializer, NewsCreateUpdateSerializer, NewsCategorySerializer


# ========== NEWS CATEGORY VIEWS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_categories(request):
    """Get all news categories"""
    categories = NewsCategory.objects.all()
    serializer = NewsCategorySerializer(categories, many=True)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    """Create a new news category (Admin only)"""
    serializer = NewsCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': 'Category created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Category creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# ========== NEWS VIEWS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_news(request):
    """Get all published news with filtering options"""
    # Get query parameters
    category_slug = request.query_params.get('category', None)
    language = request.query_params.get('language', None)
    urgency = request.query_params.get('urgency', None)
    is_event = request.query_params.get('is_event', None)
    is_research = request.query_params.get('is_research', None)
    search = request.query_params.get('search', None)
    
    # Start with published news
    news_list = News.objects.filter(is_published=True)
    
    # Apply filters
    if category_slug:
        news_list = news_list.filter(category__slug=category_slug)
    
    if language:
        news_list = news_list.filter(language=language)
    
    if urgency:
        news_list = news_list.filter(urgency=urgency)
    
    if is_event and is_event.lower() == 'true':
        news_list = news_list.filter(is_event=True)
    
    if is_research and is_research.lower() == 'true':
        news_list = news_list.filter(is_research=True)
    
    if search:
        news_list = news_list.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(content__icontains=search) |
            Q(tags__icontains=search)
        )
    
    # Order by publish date (newest first)
    news_list = news_list.order_by('-publish_date', '-created_at')
    
    serializer = NewsSerializer(news_list, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': news_list.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_news_detail(request, slug):
    """Get detailed view of a single news article"""
    news = get_object_or_404(News, slug=slug, is_published=True)
    
    # Increment view count
    news.increment_views()
    
    serializer = NewsSerializer(news, context={'request': request})
    
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_urgent_news(request):
    """Get urgent and breaking news"""
    urgent_news = News.objects.filter(
        is_published=True,
        urgency__in=['urgent', 'breaking']
    ).order_by('-publish_date')[:10]
    
    serializer = NewsSerializer(urgent_news, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': urgent_news.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_upcoming_events(request):
    """Get upcoming events"""
    upcoming_events = News.objects.filter(
        is_published=True,
        is_event=True,
        event_date__gte=timezone.now().date()
    ).order_by('event_date')[:10]
    
    serializer = NewsSerializer(upcoming_events, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': upcoming_events.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_research_news(request):
    """Get research-related news"""
    research_news = News.objects.filter(
        is_published=True,
        is_research=True
    ).order_by('-publish_date')[:10]
    
    serializer = NewsSerializer(research_news, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': research_news.count(),
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def create_news(request):
    """Create a new news article (Admin only)"""
    serializer = NewsCreateUpdateSerializer(data=request.data)
    
    if serializer.is_valid():
        news = serializer.save()
        
        # Return full news data
        full_serializer = NewsSerializer(news, context={'request': request})
        
        return Response({
            'success': True,
            'message': 'News created successfully',
            'data': full_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'News creation failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def update_news(request, id):
    """Update an existing news article (Admin only)"""
    news = get_object_or_404(News, id=id)
    
    serializer = NewsCreateUpdateSerializer(
        news, 
        data=request.data, 
        partial=True if request.method == 'PATCH' else False
    )
    
    if serializer.is_valid():
        updated_news = serializer.save()
        
        # Return full news data
        full_serializer = NewsSerializer(updated_news, context={'request': request})
        
        return Response({
            'success': True,
            'message': 'News updated successfully',
            'data': full_serializer.data
        })
    
    return Response({
        'success': False,
        'message': 'News update failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_news(request, id):
    """Delete a news article (Admin only)"""
    news = get_object_or_404(News, id=id)
    news.delete()
    
    return Response({
        'success': True,
        'message': 'News deleted successfully'
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_news_admin(request):
    """Get all news (including unpublished) for admin panel"""
    # Get query parameters
    published_only = request.query_params.get('published_only', 'false')
    
    if published_only.lower() == 'true':
        news_list = News.objects.filter(is_published=True)
    else:
        news_list = News.objects.all()
    
    news_list = news_list.order_by('-created_at')
    
    serializer = NewsSerializer(news_list, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': news_list.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_news_stats(request):
    """Get news statistics"""
    total_news = News.objects.filter(is_published=True).count()
    urgent_news = News.objects.filter(is_published=True, urgency__in=['urgent', 'breaking']).count()
    events = News.objects.filter(is_published=True, is_event=True).count()
    research = News.objects.filter(is_published=True, is_research=True).count()
    
    # Get latest news date
    latest_news = News.objects.filter(is_published=True).order_by('-publish_date').first()
    latest_date = latest_news.publish_date if latest_news else None
    
    return Response({
        'success': True,
        'stats': {
            'total_news': total_news,
            'urgent_news': urgent_news,
            'events': events,
            'research': research,
            'latest_news_date': latest_date
        }
    })