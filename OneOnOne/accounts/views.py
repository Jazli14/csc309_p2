from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from .serializers import UserAccountSerializer, ContactSerializer
from .models import UserAccount, Contact
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_endpoint(request):
    # If the user is authenticated, return a success message
    username = request.user.username

    return Response({"message": "You are verified. This is a protected endpoint.",
                     "user": username})


@api_view(['POST'])
def create_user_account(request):
    serializer = UserAccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def handle_contacts(request, user_id):
    # Get the user making the request

    if request.method == 'POST':
    
        # contact_fields = Contact._meta.fields
        # print([field.name for field in contact_fields])

        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        user = request.user

        # Check if the user is a teacher
        if user.user_type != 't':
            return Response({'error': 'Only teachers can add contacts'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user_account = UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():

            contact_id = serializer.validated_data.get('contact')

            if contact_id is None:
                return Response({'error': 'Contact ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
            if user_id == int(request.data.get('contact')[0]):
                return Response({'error': 'Cannot add yourself as a contact'}, status=status.HTTP_409_CONFLICT)

            if Contact.objects.filter(user=user_id, contact=contact_id).exists():
                return Response({'error': 'Contact already exists in the list'}, status=status.HTTP_409_CONFLICT)
            
            serializer.save(user_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'GET':
        # Get the user making the request
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve the user object
        user = get_object_or_404(UserAccount, pk=user_id)

        try:
            user = UserAccount.objects.get(id=user_id)
            if user.user_type != 't':
                return Response({'error': 'User must be a teacher'}, status=status.HTTP_400_BAD_REQUEST)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Filter contacts based on the user ID
        contacts = Contact.objects.filter(user=user_id)
        
        # Serialize the contacts
        serializer = ContactSerializer(contacts, many=True)
        
        return Response(serializer.data)
    # provided_user_id = request.data.get('user')
    
    # # If user parameter is provided and not empty, use it
    # if provided_user_id:
    #     user_id = provided_user_id
    # else:
    #     user_id = user.id
    
    # # Make a copy of the request data

    # mutable_data = request.data.copy()
    # # Assign the user ID to the 'user' field in the copied data
    # mutable_data['user'] = user_id

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def list_contacts(request, user_id):


    # # Get the user parameter from the request query parameters, if provided
    # provided_user_id = request.data['user']

    # print("PROVIDED USER_ID", provided_user_id)
    # # If user parameter is provided and not empty, use it
    # if provided_user_id:
    #     user_id = provided_user_id
    # else:
    #     user_id = user.id
    
    # # Check if the provided user is a teacher
    # print("I AM USER:", user_id)