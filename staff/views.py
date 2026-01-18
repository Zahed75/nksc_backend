from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Department, Staff
from .serializers import (
    DepartmentSerializer,
    StaffSerializer,
    StaffListSerializer
)


class StaffAPIView(APIView):
    """
    Single API endpoint for all staff operations

    GET /api/staff/ - Get all staff
    POST /api/staff/ - Create new staff
    GET /api/staff/{id}/ - Get staff by ID
    PUT /api/staff/{id}/ - Update staff
    PATCH /api/staff/{id}/ - Partial update staff
    DELETE /api/staff/{id}/ - Delete staff
    """

    def get_permissions(self):
        """Set permissions based on HTTP method"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    # ========== GET ALL STAFF ==========
    def get(self, request, id=None):
        """Get all staff or single staff by ID"""
        if id:
            return self._get_staff_by_id(id, request)
        return self._get_all_staff(request)

    def _get_all_staff(self, request):  # <-- FIXED: This should be indented inside the class
        """Get all staff with comprehensive filtering options"""
        # Build query filters dynamically
        filters = Q()

        # ===== TEXT SEARCH FILTERS =====
        search = request.query_params.get('search', None)
        if search:
            search = search.strip()
            filters &= (
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(alternate_phone__icontains=search) |
                Q(bio__icontains=search) |
                Q(qualifications__icontains=search) |
                Q(research_interests__icontains=search) |
                Q(office_room__icontains=search) |
                Q(office_hours__icontains=search)
            )

        # ===== BOOLEAN/STATUS FILTERS =====
        is_active = request.query_params.get('is_active', None)
        if is_active is not None:
            filters &= Q(is_active=is_active.lower() == 'true')

        # ===== EXACT MATCH FILTERS =====
        # Department (by ID or slug)
        department_id = request.query_params.get('department_id', None)
        department_slug = request.query_params.get('department', None)
        if department_id:
            filters &= Q(department_id=department_id)
        elif department_slug:
            filters &= Q(department__slug=department_slug)

        # Designation (exact or multiple)
        designation = request.query_params.get('designation', None)
        if designation:
            if ',' in designation:
                # Multiple designations
                designations = designation.split(',')
                filters &= Q(designation__in=designations)
            else:
                # Single designation
                filters &= Q(designation=designation)

        # Email (exact or partial)
        email = request.query_params.get('email', None)
        if email:
            filters &= Q(email__icontains=email)

        # Phone number
        phone = request.query_params.get('phone', None)
        if phone:
            filters &= Q(phone__icontains=phone)

        # ===== SOCIAL MEDIA FILTERS =====
        has_website = request.query_params.get('has_website', None)
        if has_website is not None:
            if has_website.lower() == 'true':
                filters &= ~Q(website__exact='') & ~Q(website__isnull=True)
            else:
                filters &= Q(website__exact='') | Q(website__isnull=True)

        has_linkedin = request.query_params.get('has_linkedin', None)
        if has_linkedin is not None:
            if has_linkedin.lower() == 'true':
                filters &= ~Q(linkedin__exact='') & ~Q(linkedin__isnull=True)
            else:
                filters &= Q(linkedin__exact='') | Q(linkedin__isnull=True)

        has_cv = request.query_params.get('has_cv', None)
        if has_cv is not None:
            if has_cv.lower() == 'true':
                filters &= Q(cv__isnull=False)
            else:
                filters &= Q(cv__isnull=True)

        has_profile_image = request.query_params.get('has_profile_image', None)
        if has_profile_image is not None:
            if has_profile_image.lower() == 'true':
                filters &= Q(profile_image__isnull=False)
            else:
                filters &= Q(profile_image__isnull=True)

        # ===== DATE FILTERS =====
        join_date_from = request.query_params.get('join_date_from', None)
        join_date_to = request.query_params.get('join_date_to', None)
        if join_date_from:
            filters &= Q(join_date__gte=join_date_from)
        if join_date_to:
            filters &= Q(join_date__lte=join_date_to)

        join_year = request.query_params.get('join_year', None)
        if join_year:
            filters &= Q(join_date__year=join_year)

        created_after = request.query_params.get('created_after', None)
        if created_after:
            filters &= Q(created_at__gte=created_after)

        updated_after = request.query_params.get('updated_after', None)
        if updated_after:
            filters &= Q(updated_at__gte=updated_after)

        # ===== TEXT FIELD SPECIFIC FILTERS =====
        bio_contains = request.query_params.get('bio_contains', None)
        if bio_contains:
            filters &= Q(bio__icontains=bio_contains)

        qualifications_contains = request.query_params.get(
            'qualifications_contains', None)
        if qualifications_contains:
            filters &= Q(qualifications__icontains=qualifications_contains)

        research_interests_contains = request.query_params.get(
            'research_interests_contains', None)
        if research_interests_contains:
            filters &= Q(research_interests__icontains=research_interests_contains)

        # ===== ORDERING =====
        order_by = request.query_params.get('order_by', 'display_order,name')
        # Validate order_by fields
        allowed_ordering = ['name', 'designation', 'join_date',
                            'created_at', 'updated_at', 'display_order']
        order_fields = []
        for field in order_by.split(','):
            field = field.strip()
            if field.startswith('-'):
                clean_field = field[1:]
            else:
                clean_field = field

            if clean_field in allowed_ordering:
                order_fields.append(field)

        if not order_fields:
            order_fields = ['display_order', 'name']

        # ===== APPLY FILTERS =====
        staff_list = Staff.objects.filter(filters).order_by(*order_fields)

        # ===== PAGINATION =====
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        # Validate pagination
        page = max(1, page)
        page_size = min(max(1, page_size), 100)  # Max 100 per page

        total_count = staff_list.count()
        total_pages = (total_count + page_size - 1) // page_size

        start = (page - 1) * page_size
        end = start + page_size

        paginated_staff = staff_list[start:end]

        # ===== SERIALIZE AND RESPOND =====
        serializer = StaffListSerializer(
            paginated_staff,
            many=True,
            context={'request': request}
        )

        return Response({
            'success': True,
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_previous': page > 1,
            'next_page': page + 1 if page < total_pages else None,
            'previous_page': page - 1 if page > 1 else None,
            'filters_applied': {
                'search': search,
                'department': department_slug or department_id,
                'designation': designation,
                'is_active': is_active,
                # Add other filters if needed
            },
            'data': serializer.data
        })

    def _get_staff_by_id(self, id, request):
        """Get single staff by ID"""
        staff = get_object_or_404(Staff, id=id)

        # Check if staff is active (unless admin)
        if not staff.is_active and not request.user.is_staff:
            return Response({
                'success': False,
                'message': 'Staff not found or inactive'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(staff, context={'request': request})

        return Response({
            'success': True,
            'data': serializer.data
        })

    # ========== CREATE STAFF ==========
    def post(self, request):
        """Create new staff"""
        serializer = StaffSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Staff created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'message': 'Staff creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # ========== UPDATE STAFF ==========
    def put(self, request, id=None):
        """Update staff (full update)"""
        if not id:
            return Response({
                'success': False,
                'message': 'Staff ID is required for update'
            }, status=status.HTTP_400_BAD_REQUEST)

        staff = get_object_or_404(Staff, id=id)
        serializer = StaffSerializer(
            staff, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Staff updated successfully',
                'data': serializer.data
            })

        return Response({
            'success': False,
            'message': 'Staff update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        """Update staff (partial update)"""
        if not id:
            return Response({
                'success': False,
                'message': 'Staff ID is required for update'
            }, status=status.HTTP_400_BAD_REQUEST)

        staff = get_object_or_404(Staff, id=id)
        serializer = StaffSerializer(
            staff, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Staff updated successfully',
                'data': serializer.data
            })

        return Response({
            'success': False,
            'message': 'Staff update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # ========== DELETE STAFF ==========
    def delete(self, request, id=None):
        """Delete staff"""
        if not id:
            return Response({
                'success': False,
                'message': 'Staff ID is required for deletion'
            }, status=status.HTTP_400_BAD_REQUEST)

        staff = get_object_or_404(Staff, id=id)
        staff.delete()

        return Response({
            'success': True,
            'message': 'Staff deleted successfully'
        })


class DepartmentAPIView(APIView):
    """Department API endpoints"""

    def get(self, request):
        """Get all departments"""
        departments = Department.objects.all().order_by('display_order', 'name')
        serializer = DepartmentSerializer(departments, many=True)

        return Response({
            'success': True,
            'count': departments.count(),
            'data': serializer.data
        })


class StaffStatsAPIView(APIView):
    """Staff statistics"""

    def get(self, request):
        """Get staff statistics"""
        total_staff = Staff.objects.count()
        active_staff = Staff.objects.filter(is_active=True).count()

        # Count by designation
        designation_counts = {}
        for choice in Staff.DESIGNATION_CHOICES:
            count = Staff.objects.filter(
                designation=choice[0], is_active=True).count()
            if count > 0:
                designation_counts[choice[1]] = count

        # Count by department
        department_counts = []
        departments = Department.objects.all()
        for dept in departments:
            count = dept.staff_set.filter(is_active=True).count()
            if count > 0:
                department_counts.append({
                    'id': dept.id,
                    'name': dept.name,
                    'slug': dept.slug,
                    'count': count
                })

        return Response({
            'success': True,
            'stats': {
                'total_staff': total_staff,
                'active_staff': active_staff,
                'inactive_staff': total_staff - active_staff,
                'designation_counts': designation_counts,
                'department_counts': department_counts
            }
        })