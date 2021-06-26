from django.contrib import admin
from django.urls import include, path
from core.views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('upload/<int:medical_test_option>', FileUploadView.as_view(), name='file-ipload-view'),
#     path('validate-email', csrf_exempt(EmailValidationView.as_view()),
     #     name='validate_email'),
#     path('activate/<uidb64>/<token>',
     #     VerificationView.as_view(), name='activate'),
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('medicaltest/', AddMedicalTest.as_view(), name="medicaltest"),
]
