from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Journal
from .serializers import JournalSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_journal(request):
    """
    Create a new journal (Admin/Editor only)
    """
    try:
        serializer = JournalSerializer(data=request.data)
        if serializer.is_valid():
            journal = serializer.save()
            return Response({
                "code": status.HTTP_201_CREATED,
                "message": "Journal created successfully",
                "data": JournalSerializer(journal).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Journal creation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception:
        return Response({
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal server error"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_journal(request, journal_id):
    """
    Update journal by ID
    """
    try:
        journal = Journal.objects.get(id=journal_id)
        serializer = JournalSerializer(journal, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Journal updated successfully",
                "data": serializer.data
            })

        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Journal update failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Journal.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Journal not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_all_journals(request):
    """
    Public API – list all published journals
    """
    journals = Journal.objects.filter(is_published=True).order_by("-created_at")
    serializer = JournalSerializer(journals, many=True)

    return Response({
        "code": status.HTTP_200_OK,
        "data": serializer.data
    })




@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_journal(request, journal_id):
    """
    Delete journal by ID
    """
    try:
        journal = Journal.objects.get(id=journal_id)
        journal.delete()

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Journal deleted successfully"
        })

    except Journal.DoesNotExist:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Journal not found"
        }, status=status.HTTP_404_NOT_FOUND)

