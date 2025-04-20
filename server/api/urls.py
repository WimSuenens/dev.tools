"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from api.views import PeppolValidateViewSet, PeppolToHtmlViewSet, PdfConvertToImagesViewSet, PdfConvertToBase64ImagesViewSet, OcrMyPdfViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'peppol/validate', PeppolValidateViewSet, basename="peppol_validate")
router.register(r'peppol/convert_to_html', PeppolToHtmlViewSet, basename="peppol_html")
router.register(r'pdf/convert_to_images', PdfConvertToImagesViewSet, basename="pdf_convert_to_images")
router.register(r'pdf/convert_to_base64images', PdfConvertToBase64ImagesViewSet, basename="pdf_convert_to_base64images")
router.register(r'pdf/ocr', OcrMyPdfViewSet, basename="pdf_ocr")


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('test', TestView.as_view(), name='test'),
    # API Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
