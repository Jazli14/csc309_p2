from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
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
    if request.method == 'POST':
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def modify_user_account(request, user_id):
    if request.method == 'POST':
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = request.user
        except UserAccount.DoesNotExist:
            return Response({'error': 'User account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Remove pk, username, and user_type fields from the request data
        request_data = request.data.copy()
        request_data.pop('pk', None)
        request_data.pop('username', None)
        request_data.pop('user_type', None)

        # Serialize the user account with the modified request data
        serializer = UserAccountSerializer(user, data=request_data, partial=True)
        if serializer.is_valid():
            # Update the password if provided
            if 'password' in request_data:
                serializer.validated_data['password'] = make_password(request_data['password'])

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = UserAccount.objects.get(pk=user_id)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User account not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete the user account
        user.delete()
        return Response({'message': 'User account deleted successfully'}, status=status.HTTP_200_OK)



@api_view(['GET'])
def get_current_user_id(request):
    user_id = request.user.id
    return Response({'user_id': user_id}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def handle_contacts(request, user_id):
    # Get the user making the request
    if request.method == 'POST':
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        user = request.user

        user_account = UserAccount.objects.filter(pk=user_id).first()
        if not user_account:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is a teacher
        if user.user_type != 't':
            return Response({'error': 'Only teachers can add contacts'}, status=status.HTTP_403_FORBIDDEN)

        if not request.data:
            return Response({'error': 'Request body is empty'}, status=status.HTTP_400_BAD_REQUEST)

        potential_contact = UserAccount.objects.filter(pk=request.data.get('contact')).first()
        if not potential_contact:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
        
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
    
    elif request.method == 'DELETE':
        # Ensure the requesting user is the owner of the contacts
        if request.user.id != user_id:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        if not request.data:
            return Response({'error': 'Request body is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the contact to delete
        contact_id = request.data.get('contact')

        
        try:
            contact = Contact.objects.get(user_id=user_id, contact_id=contact_id)
        except Contact.DoesNotExist:
            return Response({'error': 'Account was not a contact'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the contact
        contact.delete()
        return Response({'message': 'Contact deleted successfully'}, status=status.HTTP_200_OK)