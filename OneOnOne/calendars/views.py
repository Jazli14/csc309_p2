from django.shortcuts import render
from .models import Calendar, TimeBlock
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import CalendarSerializer, TimeBlockSerializer

# Calendar Views 
@api_view(['GET'])
def test_ping(request):
    return Response({"data": "Server is up and running."})

class CalendarListCreate(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class CalendarRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


# TimeBlock Views
class TimeBlocksListView(generics.ListAPIView):
    serializer_class = TimeBlockSerializer

    def get_queryset(self):
        calendar_id = self.kwargs['calendar_id']
        return TimeBlock.objects.filter(calendar_id=calendar_id)


class AddTimeBlockView(generics.CreateAPIView):
    serializer_class = TimeBlockSerializer

    def create(self, request, *args, **kwargs):
        calendar_id = self.kwargs['calendar_id']
        try:
            calendar = Calendar.objects.get(id=calendar_id)
        except Calendar.DoesNotExist:
            return Response({"message": "Calendar not found"}, status=status.HTTP_404_NOT_FOUND)

        request.data['calendar'] = calendar_id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EditTimeBlockView(generics.RetrieveUpdateAPIView):
    serializer_class = TimeBlockSerializer
    queryset = TimeBlock.objects.all()
    lookup_url_kwarg = 'pk'  # Using 'pk' as the default lookup field

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DeleteTimeBlockView(generics.DestroyAPIView):
    serializer_class = TimeBlockSerializer
    queryset = TimeBlock.objects.all()
    lookup_url_kwarg = 'timeblock_id'

