from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

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