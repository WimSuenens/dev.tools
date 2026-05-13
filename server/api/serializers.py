"""
API Serializers
"""

# from django.contrib.auth.models import Group, User
# from rest_framework.serializers import HyperlinkedModelSerializer, Serializer, FileField
import os
from django.forms import ValidationError
from rest_framework.serializers import Serializer, FileField, BooleanField, CharField, ChoiceField

# Serializers define the API representation.
# class UserSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'is_staff']

# class GroupSerializer(HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class AS4DocumentUploadSerializer(Serializer):
    """
    A serializer used for AS4 document validation
    """
    profile = ChoiceField(
        choices=[
            ("PEPPOL_BIS_BILLING_V3", "Peppol BIS Billing V3 - UBL 2.1"),
            ("PEPPOL_BIS_SELF_BILLING_V3", "Peppol BIS Self-Billing V3 - UBL 2.1"),
            ("SI_UBL_V2_0", "SimplerInvoicing UBL v2.0 - UBL 2.1 - NL CIUS v1.0.3"),
            ("EN16931_UBL", "EN 16931 UBL - FR CIUS"),
            ("EN16931_UBL_EXTENDED_CTC_FR", "EN 16931 UBL - FR CIUS Extended"),
            ("EN16931_CII", "EN 16931 CII - FR CIUS"),
            ("EN16931_CII_EXTENDED_CTC_FR", "EN 16931 CII - FR CIUS Extended"),
        ]
    )
    document = FileField()

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

class OCRMyPDFSerializer(Serializer):
    """
    A serializer used to OCR a PDF
    """
    pdf = FileField(validators=[validate_file_extension])
    as_attachment = BooleanField(default=True, initial=True)
    clean = BooleanField(default=True, initial=True)
    deskew = BooleanField(default=True, initial=True)
    rotate_pages = BooleanField(default=True, initial=True)
    output_type = CharField(default="pdfa", initial="pdfa")
    skip_text = BooleanField(default=True, initial=True)
    invalidate_digital_signatures = BooleanField(default=True, initial=True)
    