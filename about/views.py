from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    AboutSection, TimelineEvent, Director, 
    Facility, Statistic, ContactInfo
)
from .serializers import (
    AboutSectionSerializer, TimelineEventSerializer,
    DirectorSerializer, FacilitySerializer,
    StatisticSerializer, ContactInfoSerializer
)


class AboutAPIView(APIView):
    """Main about API endpoint"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get(self, request):
        """Get all about data in a single API call"""
        
        # Get active sections by type
        sections = AboutSection.objects.filter(is_active=True).order_by('display_order', 'title')
        
        # Get timeline events
        timeline_events = TimelineEvent.objects.filter(is_active=True).order_by('-display_order', 'year')
        
        # Get directors
        directors = Director.objects.filter(is_active=True).order_by('director_type', '-display_order', 'name')
        
        # Get facilities
        facilities = Facility.objects.filter(is_active=True).order_by('display_order', 'title')
        
        # Get statistics
        statistics = Statistic.objects.filter(is_active=True).order_by('display_order', 'label')
        
        # Get contact info
        contact_info = ContactInfo.objects.filter(is_active=True).order_by('display_order', 'contact_type')
        
        # Serialize data
        sections_data = AboutSectionSerializer(sections, many=True, context={'request': request}).data
        timeline_data = TimelineEventSerializer(timeline_events, many=True, context={'request': request}).data
        directors_data = DirectorSerializer(directors, many=True, context={'request': request}).data
        facilities_data = FacilitySerializer(facilities, many=True, context={'request': request}).data
        stats_data = StatisticSerializer(statistics, many=True).data
        contact_data = ContactInfoSerializer(contact_info, many=True).data
        
        # Group directors by type
        current_directors = [d for d in directors_data if d['director_type'] == 'current']
        previous_directors = [d for d in directors_data if d['director_type'] == 'previous']
        
        return Response({
            'success': True,
            'data': {
                'sections': sections_data,
                'timeline_events': timeline_data,
                'directors': {
                    'current': current_directors,
                    'previous': previous_directors
                },
                'facilities': facilities_data,
                'statistics': stats_data,
                'contact_info': contact_data
            }
        })
    
    def post(self, request):
        """Create multiple about data entries at once (Admin only)"""
        data = request.data
        
        response_data = {
            'sections': [],
            'timeline_events': [],
            'directors': [],
            'facilities': [],
            'statistics': [],
            'contact_info': []
        }
        
        # Create sections if provided
        if 'sections' in data and isinstance(data['sections'], list):
            for section_data in data['sections']:
                serializer = AboutSectionSerializer(data=section_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['sections'].append(serializer.data)
        
        # Create timeline events if provided
        if 'timeline_events' in data and isinstance(data['timeline_events'], list):
            for event_data in data['timeline_events']:
                serializer = TimelineEventSerializer(data=event_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['timeline_events'].append(serializer.data)
        
        # Create directors if provided
        if 'directors' in data and isinstance(data['directors'], list):
            for director_data in data['directors']:
                serializer = DirectorSerializer(data=director_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['directors'].append(serializer.data)
        
        # Create facilities if provided
        if 'facilities' in data and isinstance(data['facilities'], list):
            for facility_data in data['facilities']:
                serializer = FacilitySerializer(data=facility_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['facilities'].append(serializer.data)
        
        # Create statistics if provided
        if 'statistics' in data and isinstance(data['statistics'], list):
            for stat_data in data['statistics']:
                serializer = StatisticSerializer(data=stat_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['statistics'].append(serializer.data)
        
        # Create contact info if provided
        if 'contact_info' in data and isinstance(data['contact_info'], list):
            for contact_data in data['contact_info']:
                serializer = ContactInfoSerializer(data=contact_data)
                if serializer.is_valid():
                    serializer.save()
                    response_data['contact_info'].append(serializer.data)
        
        return Response({
            'success': True,
            'message': 'Data created successfully',
            'data': response_data
        }, status=status.HTTP_201_CREATED)


# Individual endpoints for specific data

class AboutSectionsAPIView(APIView):
    """Get about sections by type"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]
    
    def get(self, request):
        section_type = request.query_params.get('type', None)
        
        queryset = AboutSection.objects.filter(is_active=True)
        
        if section_type:
            queryset = queryset.filter(section_type=section_type)
        
        queryset = queryset.order_by('display_order', 'title')
        
        serializer = AboutSectionSerializer(queryset, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """Create a new about section"""
        serializer = AboutSectionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Section created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Section creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TimelineEventsAPIView(APIView):
    """Get timeline events"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]
    
    def get(self, request):
        events = TimelineEvent.objects.filter(is_active=True).order_by('-display_order', 'year')
        serializer = TimelineEventSerializer(events, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'count': events.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """Create a new timeline event"""
        serializer = TimelineEventSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Timeline event created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Timeline event creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DirectorsAPIView(APIView):
    """Get directors"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]
    
    def get(self, request):
        director_type = request.query_params.get('type', None)
        
        queryset = Director.objects.filter(is_active=True)
        
        if director_type:
            queryset = queryset.filter(director_type=director_type)
        
        queryset = queryset.order_by('director_type', '-display_order', 'name')
        
        serializer = DirectorSerializer(queryset, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'count': queryset.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        
        """Create a new director"""
        permission_classes = [AllowAny]
        serializer = DirectorSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Director created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Director creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CurrentDirectorAPIView(APIView):
    """Get current director"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        current_director = Director.objects.filter(
            director_type='current',
            is_active=True
        ).order_by('-display_order').first()
        
        if current_director:
            serializer = DirectorSerializer(current_director, context={'request': request})
            return Response({
                'success': True,
                'data': serializer.data
            })
        else:
            return Response({
                'success': False,
                'message': 'No current director found'
            }, status=404)


class FacilitiesAPIView(APIView):
    """Get facilities"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]
    
    def get(self, request):
        facilities = Facility.objects.filter(is_active=True).order_by('display_order', 'title')
        serializer = FacilitySerializer(facilities, many=True, context={'request': request})
        
        return Response({
            'success': True,
            'count': facilities.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """Create a new facility"""
        serializer = FacilitySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Facility created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Facility creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# Add these new views for Statistics and ContactInfo

class StatisticsAPIView(APIView):
    """Get statistics"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get(self, request):
        stats = Statistic.objects.filter(is_active=True).order_by('display_order', 'label')
        serializer = StatisticSerializer(stats, many=True)
        
        return Response({
            'success': True,
            'count': stats.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """Create a new statistic"""
        serializer = StatisticSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Statistic created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Statistic creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ContactInfoAPIView(APIView):
    """Get contact information"""
    
    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get(self, request):
        contact_info = ContactInfo.objects.filter(is_active=True).order_by('display_order', 'contact_type')
        serializer = ContactInfoSerializer(contact_info, many=True)
        
        return Response({
            'success': True,
            'count': contact_info.count(),
            'data': serializer.data
        })
    
    def post(self, request):
        """Create new contact information"""
        serializer = ContactInfoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Contact info created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Contact info creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)