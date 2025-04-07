"""Some Test"""

from base64 import b64encode
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from api.serializers import PeppolValidateSerializer
from api.utils import validate_peppol, transform_to_html
import pdfkit

# ViewSets define the view behavior.
class PeppolValidateViewSet(ViewSet):
    """
    A viewset to handle Peppol validate requests.
    """
    serializer_class = PeppolValidateSerializer

    def list(self, request: Request):
        """
        List all Peppol validate requests.
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to validate Peppol UBL files."
        print(f"STATIC_URL - {settings.STATIC_URL}")
        print(f"STATIC_ROOT - {settings.STATIC_ROOT}")
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        Validate a Peppol UBL file.
        """
        serializer = PeppolValidateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file: InMemoryUploadedFile = serializer.validated_data['ubl']

        response = validate_peppol(file)
        return Response(response, status=status.HTTP_200_OK)

class PeppolToHtmlViewSet(ViewSet):
    """
    A viewset to handle Peppol to Html requests.
    """
    serializer_class = PeppolValidateSerializer

    def list(self, request: Request):
        """
        List all Peppol validate requests.
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to visualize a Peppol UBL files."
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        Validate a Peppol UBL file.
        """
        try:
            serializer = PeppolValidateSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            file: InMemoryUploadedFile = serializer.validated_data['ubl']

            response = transform_to_html(file)
            pdf = pdfkit.from_string(response)
            base64 = b64encode(pdf).decode('utf-8')
            return Response({"base64": base64})
        except Exception as e:
            print(f"Error transforming to HTML: {e}")
            return f"<html><body>Error transforming to HTML</body></html>"

        # return Response(response, status=status.HTTP_200_OK)
