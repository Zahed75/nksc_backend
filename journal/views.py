from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import JournalPage
from .serializers import JournalSerializer


@api_view(['GET'])
def journal_list(request):
    journals = JournalPage.objects.live().public().order_by('-year', '-volume')
    serializer = JournalSerializer(journals, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def journal_create(request):
    serializer = JournalSerializer(data=request.data)
    if serializer.is_valid():
        journal = serializer.save()
        return Response({
            'code': status.HTTP_201_CREATED,
            'message': "Journal created successfully",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'code': status.HTTP_400_BAD_REQUEST,
        'message': "Journal creation failed",
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
