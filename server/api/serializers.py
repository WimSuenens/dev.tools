"""
API Serializers
"""

# from django.contrib.auth.models import Group, User
# from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, FileField
from rest_framework.serializers import Serializer, FileField

# Serializers define the API representation.
# class UserSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# class GroupSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class PeppolValidateSerializer(Serializer):
    """
    A serializer used for Peppol validation
    """
    ubl = FileField()

    # def create(self, validated_data):
    #     # Implement your creation logic here
    #     # If you don't need to create anything, just return validated_data
    #     return validated_data

    # def update(self, instance, validated_data):
    #     # Implement your update logic here
    #     # If you don't need to update anything, just return instance
    #     return instance
