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
