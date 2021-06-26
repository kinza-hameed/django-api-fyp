from core.models import Patient,MedicalTest, MedicalTestRecord, PersonalInfo
from django.shortcuts import render
from .serializers import FileSerializer,PatientSerializer, LoginSerializer, MedicalTestSerializer
from .medical_records_retrieval import CBC_OCR, do
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
import numpy 
import cv2
import json
from decimal import Decimal as D
from django.core.mail import EmailMessage, message
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth

class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):
        ocr=None
        file_serializer = FileSerializer(data = request.data)
        medical_test_option = self.kwargs.get('medical_test_option')
        
        if file_serializer.is_valid():
            file = file_serializer.validated_data.get('file')
            im = cv2.imdecode(numpy.fromstring(request.FILES['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (9,9), 0)
            thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    # Dilate to combine adjacent text contours
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
            dilate = cv2.dilate(thresh, kernel, iterations=4)

    # Find contours, highlight text areas, and extract ROIs
            cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            line_items_coordinates = []
            image=[]
            for c in cnts:
                area = cv2.contourArea(c)
                x,y,w,h = cv2.boundingRect(c)

                if y >= 500 and x <= 1000:
                    if area > 10000:
                        image = cv2.rectangle(im, (x,y), (2500, y+h), color=(255,0,255), thickness=1)
                        line_items_coordinates.append([(x,y), (2500, y+h)])

                elif y >= 2400 and x<= 2000:
                    image = cv2.rectangle(im, (x,y), (2500, y+h), color=(255,0,255), thickness=1)
                    line_items_coordinates.append([(x,y), (2500, y+h)])


            if medical_test_option == 1:
                ocr = CBC_OCR(image,line_items_coordinates)
                ocr_array = json.dumps(ocr)
                ocr_data = json.loads(ocr_array)
                # print(xyz['patName'])
                personal_info_data = PersonalInfo(
                    patient_id = Patient.objects.get(id=1),
                    medical_test_id = MedicalTest.objects.get(id=medical_test_option),
                    name = ocr_data['patName'],
                    age = ocr_data['age'],
                    gender = ocr_data['gender'],
                    report_date = ocr_data['date']
                )
                personal_info_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'HAEMOGLOBIN',
                    range_of_test = "11-14.5",
                    result = ocr_data['HAEMOGLOBIN'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'HAEMATOCRIT',
                    range_of_test = "11-14.5",
                    result = ocr_data['HAEMATOCRIT'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'RBC',
                    range_of_test = "11-14.5",
                    result = ocr_data['RBC'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'MCV',
                    range_of_test = "11-14.5",
                    result = ocr_data['MCV'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'MCH',
                    range_of_test = "11-14.5",
                    result = ocr_data['MCH'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'MCHC',
                    range_of_test = "11-14.5",
                    result = ocr_data['MCHC'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'RDW',
                    range_of_test = "11-14.5",
                    result = ocr_data['RDW'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'WBC',
                    range_of_test = "11-14.5",
                    result = ocr_data['WBC'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'NEUTROPHILS',
                    range_of_test = "11-14.5",
                    result = ocr_data['NEUTROPHILS'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'LYMPHOCYTES',
                    range_of_test = "11-14.5",
                    result = ocr_data['LYMPHOCYTES'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'EOSINOPHILS',
                    range_of_test = "11-14.5",
                    result = ocr_data['EOSINOPHILS'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'MONOCYTES',
                    range_of_test = "11-14.5",
                    result = ocr_data['MONOCYTES'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'BASOPHILS',
                    range_of_test = "11-14.5",
                    result = ocr_data['BASOPHILS'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
                
                medical_test_record_data = MedicalTestRecord(
                    personal_info_id = personal_info_data,
                    medical_test_name = 'PLATELETS',
                    range_of_test = "11-14.5",
                    result = ocr_data['PLATELETS'],
                    unit = 'g/dl'
                )
                medical_test_record_data.save()
            
        return JsonResponse(ocr, safe=False)




class Register(APIView):
    
    def post(self, request, *args, **kwargs):
        abc=None
        patient_serializer = PatientSerializer(data = request.data)

        print(patient_serializer.is_valid())
        if patient_serializer.is_valid(raise_exception = True):
            patient = Patient(
            address = patient_serializer.validated_data.get('address'),
            contact_no = patient_serializer.validated_data.get('contact_no'),
            gender = patient_serializer.validated_data.get('gender'),
            dob = patient_serializer.validated_data.get('dob'),
            p_name = patient_serializer.validated_data.get('p_name'),
            email = patient_serializer.validated_data.get('email'),
            password = patient_serializer.validated_data.get('password')
            )
            patient.save()

        return Response(abc, status=HTTP_200_OK)

class Login(APIView):
    
    def post(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(data = request.data)
        if login_serializer.is_valid(raise_exception = True):
            
            email = login_serializer.validated_data.get('email')
            password = login_serializer.validated_data.get('password')
            
            patient = Patient.objects.filter(email=email)
            print(patient[0].email)
            if email == patient[0].email:
                if password == patient[0].password:
                    message = {
			            'message': True
		            }
                else:
                    message = {
			            'message': "Enter correct password"
		            }
            else:
                message = {
			            'message': "Incorrect Email"
                }
            
            print('email: ', email,'password: ', password)
        return JsonResponse(message)


class AddMedicalTest(APIView):

    def post(self, request, *args, **kwargs):
        abc=None
        p_name = 'kinza'
        abc = do(p_name)
        medical_test_serializer = MedicalTestSerializer(data = request.data)
        if medical_test_serializer.is_valid(raise_exception = True):
            medical_test_data = MedicalTest(
                medical_test = medical_test_serializer.validated_data.get('medical_test'),
                hospital_name = medical_test_serializer.validated_data.get('hospital_name')
            )
            medical_test_data.save()
            message = {
			            'message': "Medical test added"
                }
        else:
            message = {
			            'message': "Incorrect Medical test"
                }


        # xyz = json.dumps(abc)
        # xyz = json.loads(xyz)
        # print(abc)
        # for items in range(1,2):
        #     print(xyz[items])
            # print(abc[0])
        # print(xyz[information])
        # print(xyz["patName"])
        return JsonResponse(abc, safe = False)

