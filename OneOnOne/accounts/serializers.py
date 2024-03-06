from rest_framework import serializers, status
from rest_framework.response import Response
from .models import UserAccount, Contact

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'username', 'password', 'email', 'user_type']


class ContactSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['contact', 'username', 'email']
    
    def get_username(self, obj):
        return obj.contact.username if obj.contact else None

    def get_email(self, obj):
        return obj.contact.email if obj.contact else None

    # def validate(self, data):
    #     # Check if the contact is trying to add themselves
    #     if self.context['request'].user == data.get('contact'):
    #         return Response(
    #             {"error": "You cannot add yourself as a contact."},
    #             status=status.HTTP_409_CONFLICT
    #         )
    #     return data

    # def create(self, validated_data):
    #     user_id = validated_data.pop('user_id')
    #     contact = Contact.objects.create(user_id=user_id, **validated_data)
    #     return contact


    # def validate(self, data):
    #     print("WE IN VALIDATION?")

    #     # Check if the contact already exists
    #     user_id = data.get('user_id')
    #     contact_id = data.get('contact')
    #     if Contact.objects.filter(user=user_id, contact=contact_id).exists():
    #         print("WE IN HERE?")
    #         raise serializers.ValidationError("Contact already exists in the list")
    #     print("WE OUT HEERE?")
    #     return data

