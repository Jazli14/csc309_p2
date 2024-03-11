from django.shortcuts import render
from .models import Calendar
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import CalendarSerializer

# Create your views here.
@api_view(['GET'])
def test_ping(request):
    return Response({"data": "Server is up and running."})

class CalendarListCreate(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class CalendarRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
