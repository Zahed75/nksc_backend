from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Chairman
from .serializers import ChairmanSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_chairman(request):
    """
    Get the current active chairman information
    Only GET API - All CRUD operations handled through Django admin
    """
    try:
        # Get the first active chairman ordered by display order
        # You can modify this logic if you need different selection criteria
        chairman = Chairman.objects.filter(is_active=True).order_by('display_order', '-created_at').first()

        if not chairman:
            return Response(
                {
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": "No active chairman found",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ChairmanSerializer(
            chairman,
            context={'request': request}
        )

        return Response(
            {
                "code": status.HTTP_200_OK,
                "message": "Chairman information retrieved successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while fetching chairman data",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_chairmen(request):
    """
    Get all active chairmen (optional - if you want to list all)
    """
    try:
        chairmen = Chairman.objects.filter(is_active=True).order_by('display_order', '-created_at')

        serializer = ChairmanSerializer(
            chairmen,
            many=True,
            context={'request': request}
        )

        return Response(
            {
                "code": status.HTTP_200_OK,
                "message": "Chairmen retrieved successfully",
                "data": serializer.data,
                "count": chairmen.count()
            },
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "An error occurred while fetching chairmen",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )