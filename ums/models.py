from django.db import models
from django.contrib.auth.models import Permission
from django.core.validators import MaxValueValidator

GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other','Other')
    )
BLOOD = (
    ('A+','A+'),
    ('A-','A-'),
    ('B+','B+'),
    ('B-','B-'),
    ('O+','O+'),
    ('O-','O-'),
    ('AB+','AB+')

)
# Create your models here.
class Doctor(models.Model):
    uname = models.CharField('Name',max_length=100, unique = True)
    name = models.CharField('Username',max_length=30)
    email = models.EmailField('Email',max_length = 100)
    password = models.CharField('Password',max_length = 300, unique =True)
    address = models.CharField('Address',max_length = 50)
    contact = models.IntegerField('Contact', validators = [MaxValueValidator(9999999999)])
    dob = models.DateField('Event Date')
    speciality = models.CharField('Speciality',max_length = 100)
    gender = models.CharField('Gender',max_length = 20, choices = GENDER)
    blood = models.CharField('Blood',max_length = 10, choices = BLOOD)

    class Meta:
        db_table = 'Doctor'
        ordering = ['name']

    def __str__(self):
        return self.name
    # files = models.ImageField(upload_to = 'profiles')

class Patient(models.Model):
    name = models.CharField('Patient Name',max_length=30)
    email = models.EmailField('Email' ,max_length = 90)
    address = models.CharField('Address',max_length = 50)
    contact = models.IntegerField('Contact', validators = [MaxValueValidator(9999999999)])
    dob = models.DateField('Date of Birth')
    gender = models.CharField('Gender',max_length = 20, choices=GENDER)
    blood = models.CharField('Blood',max_length = 10,choices=BLOOD)
    is_deleted = models.BooleanField('is_deleted', default = False, editable=False)

    class Meta:
        db_table = 'Patient'
        ordering = ['name']

    def __str__(self):
        return self.name

class Receptionist(models.Model):
    uname = models.CharField('Userame',max_length=100, unique = True)
    name = models.CharField('Full Name',max_length=30)
    email = models.EmailField('Email' ,max_length = 100)
    password = models.CharField('Password',max_length = 300, unique =True)
    address = models.CharField('Address',max_length = 50)
    contact = models.IntegerField('Contact', validators = [MaxValueValidator(9999999999)])
    dob = models.DateField('Date of Birth')
    gender = models.CharField('Gender',max_length = 20,choices=GENDER)
    blood = models.CharField('Blood',max_length = 10,choices=BLOOD)

    class Meta:
        db_table = "Receptionist"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Prescription(models.Model):
    p_id = models.IntegerField('Patient ID')
    name = models.CharField('Name', max_length=50)
    prescription =models.CharField('Prescription', max_length=300)
    date = models.DateField('Date')

    class Meta: 
        db_table = "Prescription"
        ordering = ["-date"]
        
    def __str__(self):
        return self.name

# class Prescription_Trash(models.Model):
#     p_id = models.IntegerField('Patient ID')
#     name = models.CharField('Name', max_length=50)
#     prescription =models.CharField('Prescription', max_length=300)
#     date = models.DateField('Date')
#     is_deleted = models.BooleanField('is_deleted')

#     class Meta: 
#         db_table = "trash"
#         ordering = ["-date"]
        
#     def __str__(self):
#         return self.name

class Patient_trash(models.Model):
    name = models.CharField('Patient Name',max_length=30)
    email = models.EmailField('Email' ,max_length = 100)
    address = models.CharField('Address',max_length = 50)
    contact = models.IntegerField('Contact', validators = [MaxValueValidator(9999999999)])
    dob = models.DateField('Date of Birth')
    gender = models.CharField('Gender',max_length = 20, choices=GENDER)
    blood = models.CharField('Blood',max_length = 10,choices=BLOOD)
    is_deleted = models.BooleanField('is_deleted', default = False, editable = False)

    class Meta:
        db_table = 'Patient_trash'
        ordering = ['name']

    def __str__(self):
        return self.name
