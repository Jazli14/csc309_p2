from django.shortcuts import render

from accounts.models import UserAccount
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
@permission_classes([IsAuthenticated])
def test_ping(request):
    return Response({"data": "Server is up and running."})

@permission_classes([IsAuthenticated])
class CalendarListCreate(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

@permission_classes([IsAuthenticated])
class CalendarRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer


@permission_classes([IsAuthenticated])
class CalendarAddStudent(generics.GenericAPIView):
    serializer_class = CalendarSerializer
    
    def patch(self, request, *args, **kwargs):
        calendar_id = kwargs.get('pk')  
        student_user_id = request.data.get('student_user_id')
        
        if not student_user_id:
            return Response({"error": "need student id"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            calendar = Calendar.objects.get(id=calendar_id)
            student = UserAccount.objects.get(user__id=student_user_id)
            if student.user_type == "t":
                return Response({"error": "can't add a teacher"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Calendar.DoesNotExist:
            return Response({"error": "calendar not found"}, status=status.HTTP_404_NOT_FOUND)
        except UserAccount.DoesNotExist:
            return Response({"error": "student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        calendar.students.add(student)
        calendar.save()  
        
        student_data = {
            "id": student.id,
            "username": student.username
        }
        
        return Response({
            "success": "Student added to calendar",
            "student": student_data
        }, status=status.HTTP_200_OK)



# TimeBlock Views
@permission_classes([IsAuthenticated])
class TimeBlocksListView(generics.ListAPIView):
    serializer_class = TimeBlockSerializer

    def get_queryset(self):
        calendar_id = self.kwargs['calendar_id']
        return TimeBlock.objects.filter(calendar_id=calendar_id)

@permission_classes([IsAuthenticated])
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

@permission_classes([IsAuthenticated])
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

@permission_classes([IsAuthenticated])
class DeleteTimeBlockView(generics.DestroyAPIView):
    serializer_class = TimeBlockSerializer
    queryset = TimeBlock.objects.all()
    lookup_url_kwarg = 'timeblock_id'

