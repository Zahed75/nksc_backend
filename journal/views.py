from rest_framework.decorators import permission_classes, api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Max, Min, Q, Sum, Avg
from django.core.paginator import Paginator
from datetime import datetime
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)

from .models import Journal
from .serializers import JournalSerializer


class JournalCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=JournalSerializer,
        responses={201: JournalSerializer},
        summary="Create Journal",
        description="Create a journal with PDF upload (multipart/form-data)",
    )
    def post(self, request):
        serializer = JournalSerializer(
            data=request.data,
            context={"request": request},  # Request context is passed here
        )

        if serializer.is_valid():
            journal = serializer.save()
            return Response(
                {
                    "code": status.HTTP_201_CREATED,
                    "message": "Journal created successfully",
                    "data": JournalSerializer(
                        journal,
                        context={"request": request},  # Request context is passed here
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Journal creation failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class JournalUpdateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=JournalSerializer,
        responses={200: JournalSerializer},
        parameters=[
            OpenApiParameter(
                name="journal_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="Journal ID",
            )
        ],
        summary="Update Journal",
        description="Update journal with optional PDF replacement",
    )
    def put(self, request, journal_id):
        try:
            journal = Journal.objects.get(id=journal_id)
        except Journal.DoesNotExist:
            return Response(
                {"code": status.HTTP_404_NOT_FOUND, "message": "Journal not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = JournalSerializer(journal, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Journal updated successfully",
                    "code": status.HTTP_200_OK,
                    "data": serializer.data,
                }
            )

        return Response(
            {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Journal update failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class JournalListAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: JournalSerializer(many=True)},
        summary="List Journals",
        description="Public API – list all published journals",
    )
    def get(self, request):
        journals = Journal.objects.filter(is_published=True).order_by("-created_at")
        
        # Pass request context to serializer
        serializer = JournalSerializer(
            journals, 
            many=True, 
            context={"request": request}  # ADD THIS LINE
        )
        
        return Response(
            {
                "message": "Journals retrieved successfully",
                "code": status.HTTP_200_OK,
                "data": serializer.data,
            }
        )


class JournalDeleteAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="journal_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="Journal ID",
            )
        ],
        responses={200: None},
        summary="Delete Journal",
        description="Delete journal by ID",
    )
    def delete(self, request, journal_id):
        try:
            journal = Journal.objects.get(id=journal_id)
            journal.delete()
            return Response(
                {
                    "code": status.HTTP_200_OK,
                    "message": "Journal deleted successfully",
                }
            )
        except Journal.DoesNotExist:
            return Response(
                {"code": status.HTTP_404_NOT_FOUND, "message": "Journal not found"},
                status=status.HTTP_404_NOT_FOUND,
            )






@api_view(['GET'])
@permission_classes([AllowAny])
def filter_journals(request):

    try:

        base_query = Journal.objects.all()

        # Default to published only unless explicitly requested
        is_published_param = request.query_params.get('is_published')
        if is_published_param is None or is_published_param.lower() == 'true':
            base_query = base_query.filter(is_published=True)
        elif is_published_param.lower() == 'false':
            base_query = base_query.filter(is_published=False)

        # ========== 2. APPLY BASIC FILTERS ==========
        filters = Q()

        # Single year filter
        year = request.query_params.get('year')
        if year and year.isdigit():
            filters &= Q(year=int(year))

        # Multiple years filter
        years_param = request.query_params.get('years')
        if years_param:
            years_list = [y.strip() for y in years_param.split(',') if y.strip().isdigit()]
            if years_list:
                filters &= Q(year__in=[int(y) for y in years_list])

        # Year range filter
        year_from = request.query_params.get('year_from')
        year_to = request.query_params.get('year_to')
        if year_from and year_from.isdigit():
            filters &= Q(year__gte=int(year_from))
        if year_to and year_to.isdigit():
            filters &= Q(year__lte=int(year_to))

        # Volume filter (single)
        volume = request.query_params.get('volume')
        if volume:
            filters &= Q(volume__icontains=volume)

        # Multiple volumes filter
        volumes_param = request.query_params.get('volumes')
        if volumes_param:
            volumes_list = [v.strip() for v in volumes_param.split(',') if v.strip()]
            if volumes_list:
                filters &= Q(volume__in=volumes_list)

        # Issue filter
        issue = request.query_params.get('issue')
        if issue:
            filters &= Q(issue__icontains=issue)

        # Editor filter (single)
        editor = request.query_params.get('editor')
        if editor:
            filters &= Q(editor__icontains=editor)

        # Multiple editors filter
        editors_param = request.query_params.get('editors')
        if editors_param:
            editors_list = [e.strip() for e in editors_param.split(',') if e.strip()]
            if editors_list:
                filters &= Q(editor__in=editors_list)

        # ISSN filter
        issn = request.query_params.get('issn')
        if issn:
            filters &= Q(issn__icontains=issn)

        # Pages range filter
        pages_min = request.query_params.get('pages_min')
        pages_max = request.query_params.get('pages_max')
        if pages_min and pages_min.isdigit():
            filters &= Q(pages__gte=int(pages_min))
        if pages_max and pages_max.isdigit():
            filters &= Q(pages__lte=int(pages_max))

        # File size range filter
        file_size_min = request.query_params.get('file_size_min')
        file_size_max = request.query_params.get('file_size_max')
        try:
            if file_size_min:
                filters &= Q(file_size_mb__gte=float(file_size_min))
            if file_size_max:
                filters &= Q(file_size_mb__lte=float(file_size_max))
        except (ValueError, TypeError):
            pass

        # Date range filter for created_at
        created_after = request.query_params.get('created_after')
        created_before = request.query_params.get('created_before')
        if created_after:
            try:
                created_after_date = datetime.strptime(created_after, '%Y-%m-%d').date()
                filters &= Q(created_at__date__gte=created_after_date)
            except ValueError:
                pass
        if created_before:
            try:
                created_before_date = datetime.strptime(created_before, '%Y-%m-%d').date()
                filters &= Q(created_at__date__lte=created_before_date)
            except ValueError:
                pass

        # Search across multiple fields
        search_query = request.query_params.get('search')
        if search_query:
            search_filters = Q()
            search_fields = ['title', 'description', 'volume', 'editor', 'issue', 'issn']
            for field in search_fields:
                search_filters |= Q(**{f'{field}__icontains': search_query})
            filters &= search_filters

        # Apply all filters
        journals = base_query.filter(filters)

        # ========== 3. SORTING ==========
        sort_by = request.query_params.get('sort_by', '-year')
        sort_order = request.query_params.get('sort_order')

        # Map sort fields to actual model fields
        sort_mapping = {
            'year': 'year',
            '-year': '-year',
            'title': 'title',
            '-title': '-title',
            'created_at': 'created_at',
            '-created_at': '-created_at',
            'volume': 'volume',
            '-volume': '-volume',
            'pages': 'pages',
            '-pages': '-pages',
            'file_size': 'file_size_mb',
            '-file_size': '-file_size_mb',
            'editor': 'editor',
            '-editor': '-editor'
        }

        # Handle sort_order parameter
        if sort_order and sort_by in sort_mapping:
            if sort_order.lower() == 'desc':
                sort_field = f'-{sort_mapping[sort_by].lstrip("-")}'
            else:
                sort_field = sort_mapping[sort_by].lstrip('-')
        else:
            sort_field = sort_mapping.get(sort_by, '-year')

        # Apply sorting
        journals = journals.order_by(sort_field)

        # ========== 4. CHECK IF ONLY STATISTICS ARE NEEDED ==========
        summary_only = request.query_params.get('summary', 'false').lower() == 'true'

        if summary_only:
            # Return only statistics without journal data
            stats = _calculate_statistics(journals)
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Journal statistics retrieved successfully",
                "data": {
                    "statistics": stats,
                    "filters_applied": _get_applied_filters(request)
                }
            })

        # ========== 5. PAGINATION ==========
        return_all = request.query_params.get('all', 'false').lower() == 'true'
        page_data = None

        if not return_all:
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 10)

            try:
                page = int(page)
                page_size = int(page_size)
                if page < 1:
                    page = 1
                if page_size < 1:
                    page_size = 10
                if page_size > 100:  # Limit page size
                    page_size = 100
            except ValueError:
                page = 1
                page_size = 10

            paginator = Paginator(journals, page_size)
            journal_page = paginator.get_page(page)
            journals_to_serialize = journal_page.object_list

            page_data = {
                "current_page": journal_page.number,
                "total_pages": paginator.num_pages,
                "total_items": paginator.count,
                "has_next": journal_page.has_next(),
                "has_previous": journal_page.has_previous(),
                "page_size": page_size,
                "start_index": journal_page.start_index(),
                "end_index": journal_page.end_index()
            }
        else:
            journals_to_serialize = journals
            page_data = {
                "current_page": 1,
                "total_pages": 1,
                "total_items": journals.count(),
                "has_next": False,
                "has_previous": False,
                "page_size": journals.count(),
                "start_index": 1,
                "end_index": journals.count()
            }

        # ========== 6. SERIALIZE DATA ==========
        serializer = JournalSerializer(
            journals_to_serialize,
            many=True,
            context={'request': request}
        )

        # ========== 7. PREPARE RESPONSE ==========
        response_data = {
            "code": status.HTTP_200_OK,
            "message": "Journals filtered successfully",
            "data": serializer.data,
            "pagination": page_data,
            "filters_applied": _get_applied_filters(request),
            "sorting": {
                "field": sort_field,
                "order": "desc" if sort_field.startswith('-') else "asc"
            }
        }

        # ========== 8. ADD STATISTICS IF REQUESTED ==========
        include_stats = request.query_params.get('stats', 'false').lower() == 'true'
        if include_stats:
            response_data["statistics"] = _calculate_statistics(journals)

        # ========== 9. ADD CATEGORIES IF REQUESTED ==========
        include_categories = request.query_params.get('categories', 'false').lower() == 'true'
        if include_categories:
            response_data["categories"] = _calculate_categories(journals)

        # ========== 10. ADD SUMMARY INFO ==========
        response_data["summary"] = {
            "total_found": journals.count(),
            "query_time": datetime.now().isoformat(),
            "search_performed": bool(search_query)
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while filtering journals",
                "error": str(e),
                "filters_applied": _get_applied_filters(request) if 'request' in locals() else None
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def _calculate_statistics(journals_queryset):
    """Helper function to calculate statistics from a queryset"""
    stats = journals_queryset.aggregate(
        total_count=Count('id'),
        year_min=Min('year'),
        year_max=Max('year'),
        total_pages=Sum('pages'),
        avg_pages=Avg('pages'),
        total_file_size=Sum('file_size_mb'),
        avg_file_size=Avg('file_size_mb'),
        latest_date=Max('created_at'),
        oldest_date=Min('created_at')
    )

    # Year distribution
    year_distribution = journals_queryset.values('year').annotate(
        count=Count('id'),
        latest=Max('created_at')
    ).order_by('-year')

    # Editor distribution (top 10)
    editor_distribution = journals_queryset.values('editor').annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    # Volume distribution
    volume_distribution = journals_queryset.values('volume').annotate(
        count=Count('id')
    ).order_by('volume')

    # Published status (if mixed)
    published_stats = journals_queryset.values('is_published').annotate(
        count=Count('id')
    )

    return {
        "overall": {
            "total_journals": stats['total_count'] or 0,
            "year_range": {
                "min": stats['year_min'],
                "max": stats['year_max']
            },
            "pages": {
                "total": stats['total_pages'] or 0,
                "average": round(stats['avg_pages'] or 0, 2)
            },
            "file_size": {
                "total_mb": round(stats['total_file_size'] or 0, 2),
                "average_mb": round(stats['avg_file_size'] or 0, 2)
            },
            "date_range": {
                "oldest": stats['oldest_date'],
                "latest": stats['latest_date']
            }
        },
        "distribution": {
            "by_year": list(year_distribution),
            "by_editor": list(editor_distribution),
            "by_volume": list(volume_distribution),
            "by_published_status": list(published_stats)
        }
    }


def _calculate_categories(journals_queryset):
    """Helper function to calculate category breakdown"""
    categories = {
        "years": {
            "count": journals_queryset.values('year').distinct().count(),
            "list": list(journals_queryset.values_list('year', flat=True).distinct().order_by('-year'))
        },
        "volumes": {
            "count": journals_queryset.values('volume').distinct().count(),
            "list": list(journals_queryset.values_list('volume', flat=True).distinct().order_by('volume'))
        },
        "editors": {
            "count": journals_queryset.values('editor').distinct().count(),
            "list": list(journals_queryset.values_list('editor', flat=True).distinct().order_by('editor'))
        },
        "issues": {
            "count": journals_queryset.values('issue').distinct().count(),
            "list": list(journals_queryset.values_list('issue', flat=True).distinct().order_by('issue'))
        }
    }
    return categories


def _get_applied_filters(request):
    """Helper function to extract applied filters from request"""
    applied_filters = {}

    # List of all possible filter parameters
    filter_params = [
        'year', 'years', 'year_from', 'year_to',
        'volume', 'volumes',
        'issue',
        'editor', 'editors',
        'issn',
        'is_published',
        'search',
        'pages_min', 'pages_max',
        'file_size_min', 'file_size_max',
        'created_after', 'created_before'
    ]

    for param in filter_params:
        value = request.query_params.get(param)
        if value:
            applied_filters[param] = value

    return applied_filters