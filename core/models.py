from django.db import models
from django.db.models.fields.related import ForeignKey
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


GENDER_CHOICES = (
   ('Male', 'Male'),
   ('Female', 'Female'),
   ('Other', 'Other')
)

# Create your models here.
class Patient(models.Model):
    p_name = models.CharField(max_length = 50, null = False)
    address = models.CharField(max_length = 254,  null = False)
    contact_no = models.IntegerField(validators=[MaxValueValidator(99999999999)],blank = False)
    dob = models.DateField(null = False)
    gender = models.CharField(choices = GENDER_CHOICES, max_length = 128, null = False)
    email = models.EmailField(max_length = 254, null = False)
    password = models.CharField(max_length = 25, null = False)


    class Meta:
        db_table = 'Patient'
    
class MedicalTest(models.Model):
    medical_test = models.CharField(max_length=50, null=False)
    hospital_name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'MedicalTest'


class PersonalInfo(models.Model):
    patient_id = ForeignKey(Patient, on_delete=models.CASCADE)
    medical_test_id = ForeignKey(MedicalTest, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=50, null=False)
    report_date = models.DateField(null=False)

    class Meta:
        db_table = 'PersonalInfo'

class MedicalTestRecord(models.Model):
    personal_info_id = ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    medical_test_name = models.CharField(max_length=50, null=True)
    range_of_test = models.CharField(max_length=50, null=True)
    result = models.DecimalField(max_digits=20, decimal_places=4)
    unit = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'MedicalTestRecord'
