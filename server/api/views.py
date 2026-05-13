"""Some Test"""

import io
import base64
import zipfile
from pathlib import Path
from base64 import b64encode
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, FileResponse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from api.serializers import AS4DocumentUploadSerializer, PeppolUploadSerializer, PdfUploadSerializer, OCRMyPDFSerializer
from api.utils import validate_en16931_ubl ,validate_peppol_billing, validate_peppol_self_billing, validate_peppol_si_ubl, validate_peppol_nlcius_cii, validate_en16931_extended_ctc_fr_ubl, transform_to_html, validate_en16931_cii, validate_en16931_extended_ctc_fr_cii
import pdfkit
import pdf2image
import ocrmypdf
from werkzeug.utils import secure_filename

class AS4DocumentValidateViewSet(ViewSet):
    """
    A viewset to handle Peppol validate requests.
    """
    serializer_class = AS4DocumentUploadSerializer


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
        serializer = AS4DocumentUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file: InMemoryUploadedFile = serializer.validated_data['document']
        profile: str = serializer.validated_data['profile']

        print(f"PROFILE - {profile}")

        match profile:
            case "PEPPOL_BIS_BILLING_V3" | "PEPPOL_BIS_BILLING_V3_UBL_INVOICE" | "PEPPOL_BIS_BILLING_V3_UBL_CREDIT_NOTE":
                response = validate_peppol_billing(file)
            case "PEPPOL_BIS_SELF_BILLING_V3" | "PEPPOL_BIS_SELF_BILLING_V3_UBL_INVOICE" | "PEPPOL_BIS_SELF_BILLING_V3_UBL_CREDIT_NOTE":
                response = validate_peppol_self_billing(file)
            case "SI_UBL_V2_0":
                response = validate_peppol_si_ubl(file)
            case "EN16931_UBL":
                response = validate_en16931_ubl(file)
            case "EN16931_UBL_EXTENDED_CTC_FR":
                response = validate_en16931_extended_ctc_fr_ubl(file)
            case "EN16931_CII":
                response = validate_en16931_cii(file)
            case "EN16931_CII_EXTENDED_CTC_FR":
                response = validate_en16931_extended_ctc_fr_cii(file)
            case _:
                return Response(
                    {"error": f"Unsupported variant - {profile}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(response, status=status.HTTP_200_OK)
    

# ViewSets define the view behavior.
class PeppolValidateViewSet(ViewSet):
    """
    A viewset to handle Peppol validate requests.
    """
    serializer_class = PeppolUploadSerializer

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
        serializer = PeppolUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file: InMemoryUploadedFile = serializer.validated_data['ubl']

        response = validate_peppol_billing(file)
        return Response(response, status=status.HTTP_200_OK)

class PeppolValidateBillingViewSet(ViewSet):
    """
    A viewset to handle Peppol validate requests.
    """
    serializer_class = PeppolUploadSerializer

    def list(self, request: Request):
        """
        List all Peppol validate requests.
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to validate Peppol BIS Billing UBL files."
        print(f"STATIC_URL - {settings.STATIC_URL}")
        print(f"STATIC_ROOT - {settings.STATIC_ROOT}")
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        Validate a Peppol UBL file.
        """
        serializer = PeppolUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file: InMemoryUploadedFile = serializer.validated_data['ubl']

        response = validate_peppol_billing(file)
        return Response(response, status=status.HTTP_200_OK)

class PeppolValidateSelfBillingViewSet(ViewSet):
    """
    A viewset to handle Peppol validate requests.
    """
    serializer_class = PeppolUploadSerializer

    def list(self, request: Request):
        """
        List all Peppol validate requests.
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to validate Peppol BIS Self Billing UBL files."
        print(f"STATIC_URL - {settings.STATIC_URL}")
        print(f"STATIC_ROOT - {settings.STATIC_ROOT}")
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        Validate a Peppol BIS Self Billing UBL file.
        """
        serializer = PeppolUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file: InMemoryUploadedFile = serializer.validated_data['ubl']

        response = validate_peppol_self_billing(file)
        return Response(response, status=status.HTTP_200_OK)

class PeppolToHtmlViewSet(ViewSet):
    """
    A viewset to handle Peppol to Html requests.
    """
    serializer_class = PeppolUploadSerializer

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
            serializer = PeppolUploadSerializer(data=request.data)

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

class PdfConvertToImagesViewSet(ViewSet):
    """
    A viewset to handle Pdf to Images (zip) requests.
    """
    serializer_class = PdfUploadSerializer

    def list(self, request: Request):
        """
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to convert a PDF file."
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        Convert PDF to images and return ZIP archive.
        """
        try:
            serializer = PdfUploadSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            pdf: InMemoryUploadedFile = serializer.validated_data['pdf']
            file = secure_filename(pdf.name)
            filename = Path(file).stem

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                pages = pdf2image.convert_from_bytes(pdf.read(), fmt='jpeg')
                for index, page in enumerate(pages):
                    img_buffer = io.BytesIO()
                    page.save(img_buffer, format='JPEG')
                    img_buffer.seek(0) 
                    zip_file.writestr(f"{filename}_{index}.jpg", img_buffer.getvalue())

            zip_buffer.seek(0)
            response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{filename}.zip"'
            
            return response
            # return Response({"hello": "world"})
        except Exception as e:
            return f"<html><body>Error converting to PDF</body></html>"

class PdfConvertToBase64ImagesViewSet(ViewSet):
    """
    A viewset to handle Peppol to Pdf requests.
    """
    serializer_class = PdfUploadSerializer

    def list(self, request: Request):
        """
        List all Peppol validate requests.
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to convert a PDF file."
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        Convert PDF to images and base64 array.
        """
        try:
            serializer = PdfUploadSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            pdf: InMemoryUploadedFile = serializer.validated_data['pdf']

            encoded_list = []

            pages = pdf2image.convert_from_bytes(pdf.read(), fmt='jpeg')
            for index, page in enumerate(pages):
                img_buffer = io.BytesIO()
                page.save(img_buffer, format='JPEG')
                img_buffer.seek(0)
                encoded_string = base64.b64encode(img_buffer.read()).decode("ascii")
                encoded_list.append(encoded_string)
            return Response(encoded_list, status=status.HTTP_200_OK)
        except Exception as e:
            return f"<html><body>Error converting to PDF</body></html>"

class OcrMyPdfViewSet(ViewSet):
    """
    A viewset to OCR a PDF file.
    """
    serializer_class = OCRMyPDFSerializer

    def list(self, request: Request):
        """
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to OCR a PDF."
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        """
        try:
            serializer = OCRMyPDFSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            pdf: InMemoryUploadedFile = serializer.validated_data['pdf']
            content_type = pdf.content_type
            as_attachment = serializer.validated_data['as_attachment']
            filename = secure_filename(pdf.name)

            pdf_data = pdf.read()
            input_buffer = io.BytesIO(pdf_data)
            output_buffer = io.BytesIO()

            ocrmypdf.ocr(
                input_buffer,
                output_buffer,
                clean=True,
                deskew=True,
                rotate_pages=True,
                image_dpi=300,
                output_type="pdfa",
                sidecar="-",
                skip_text=True,
                invalidate_digital_signatures=True
            )
            output_buffer.seek(0)
            return FileResponse(
                output_buffer,
                as_attachment=as_attachment,
                filename=filename,
                content_type=content_type
            )
            # response = HttpResponse(output_buffer, content_type='application/pdf')
            # response['Content-Disposition'] = f'attachment; filename="{filename}"'
            # return response
        except Exception as e:
            return Response(f"<html><body>Error converting to PDF : {e}</body></html>", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PdfExtractTextViewSet(ViewSet):
    """
    A viewset to OCR a PDF file.
    """
    serializer_class = PdfUploadSerializer

    def list(self, request: Request):
        """
        """
        username = request.user.username or "anonymous"
        message = f"Hi {username}, welcome at the endpoint to OCR a PDF."
        return Response(message, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        """
    
        try:
            serializer = PdfUploadSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            pdf: InMemoryUploadedFile = serializer.validated_data['pdf']

            return Response("encoded_list", status=status.HTTP_200_OK)
        except Exception as e:
            return f"<html><body>Error converting to PDF</body></html>"