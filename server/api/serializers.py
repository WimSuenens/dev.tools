"""
API Serializers
"""

# from django.contrib.auth.models import Group, User
# from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, FileField
import os
from django.forms import ValidationError
from rest_framework.serializers import Serializer, FileField, BooleanField

# Serializers define the API representation.
# class UserSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# class GroupSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class PeppolUploadSerializer(Serializer):
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

def validate_file_extension(value):
    """"
    Validate the file extension of the uploaded file.
    """
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext in valid_extensions:
        raise ValidationError('File not supported!')

class PdfUploadSerializer(Serializer):
    """
    A serializer used for PDF conversion
    """
    pdf = FileField(validators=[validate_file_extension])
    