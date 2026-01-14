from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify

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
# @permission_classes([IsAdminUser])
def create_category(request):
    """Create a new news category (Admin only)"""
    serializer = NewsCategorySerializer(data=request.data)
    if serializer.is_valid():
        # Generate slug if not provided
        validated_data = serializer.validated_data
        name = validated_data.get('name', '')
        
        if not validated_data.get('slug'):
            validated_data['slug'] = slugify(name)
            
        # Ensure slug is unique
        base_slug = validated_data['slug']
        counter = 1
        while NewsCategory.objects.filter(slug=validated_data['slug']).exists():
            validated_data['slug'] = f"{base_slug}-{counter}"
            counter += 1
            
        # Create the category
        category = NewsCategory.objects.create(**validated_data)
        
        return Response({
            'success': True,
            'message': 'Category created successfully',
            'data': NewsCategorySerializer(category).data
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
@parser_classes([MultiPartParser, FormParser])
def create_news(request):
    """Create a new news article (Admin only)"""
    serializer = NewsCreateUpdateSerializer(data=request.data)
    
    if serializer.is_valid():
        # Let the serializer handle slug generation and object creation
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
# @permission_classes([IsAdminUser])
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
        validated_data = serializer.validated_data
        
        # Auto-generate new slug if title is being updated
        if 'title' in validated_data and validated_data['title'] != news.title:
            title = validated_data['title']
            slug = slugify(title)
            
            # Ensure slug is unique (excluding current instance)
            base_slug = slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(id=news.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            validated_data['slug'] = slug
        
        # Update the news object
        for attr, value in validated_data.items():
            setattr(news, attr, value)
        
        news.save()
        
        # Return full news data
        full_serializer = NewsSerializer(news, context={'request': request})
        
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
# @permission_classes([IsAdminUser])
def delete_news(request, id):
    """Delete a news article (Admin only)"""
    news = get_object_or_404(News, id=id)
    news.delete()
    
    return Response({
        'success': True,
        'message': 'News deleted successfully'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_news_admin(request):
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
    
    # Apply filters with proper normalization
    if category_slug:
        # Convert to lowercase and trim
        category_slug = category_slug.strip().lower()
        
        # Try to find category by slug or name
        try:
            # First try exact slug match
            category = NewsCategory.objects.filter(slug=category_slug).first()
            
            # If not found by slug, try by name (case-insensitive)
            if not category:
                category = NewsCategory.objects.filter(name__iexact=category_slug).first()
            
            # If category found, filter news by it
            if category:
                news_list = news_list.filter(category=category)
            else:
                # If no category found, return empty
                return Response({
                    'message': 'Admin news fetch successfully',
                    'success': True,
                    'count': 0,
                    'data': [],
                    'message': f'Category "{category_slug}" not found'
                })
                
        except Exception as e:
            # Log error but continue without category filter
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error filtering by category: {e}")
    
    if language:
        # Convert to lowercase and trim
        language = language.strip().lower()
        news_list = news_list.filter(language=language)
    
    if urgency:
        # Convert to lowercase and trim
        urgency = urgency.strip().lower()
        # Handle different urgency formats
        if urgency == 'urgent news':
            urgency = 'urgent'
        elif urgency == 'breaking news':
            urgency = 'breaking'
        news_list = news_list.filter(urgency=urgency)
    
    if is_event:
        # Handle boolean string values
        is_event = is_event.strip().lower()
        if is_event in ['true', '1', 'yes']:
            news_list = news_list.filter(is_event=True)
        elif is_event in ['false', '0', 'no']:
            news_list = news_list.filter(is_event=False)
    
    if is_research:
        # Handle boolean string values
        is_research = is_research.strip().lower()
        if is_research in ['true', '1', 'yes']:
            news_list = news_list.filter(is_research=True)
        elif is_research in ['false', '0', 'no']:
            news_list = news_list.filter(is_research=False)
    
    if search:
        search = search.strip()
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
        'data': serializer.data,
        
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


# ========== ADDITIONAL UTILITY ENDPOINTS ==========

@api_view(['GET'])
@permission_classes([AllowAny])
def get_news_by_category(request, category_slug):
    """Get news by category slug"""
    category = get_object_or_404(NewsCategory, slug=category_slug)
    news_list = News.objects.filter(
        category=category,
        is_published=True
    ).order_by('-publish_date')
    
    serializer = NewsSerializer(news_list, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'category': NewsCategorySerializer(category).data,
        'count': news_list.count(),
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_latest_news(request):
    """Get latest news (limit: 10)"""
    latest_news = News.objects.filter(
        is_published=True
    ).order_by('-publish_date')[:10]
    
    serializer = NewsSerializer(latest_news, many=True, context={'request': request})
    
    return Response({
        'success': True,
        'count': latest_news.count(),
        'data': serializer.data
    })