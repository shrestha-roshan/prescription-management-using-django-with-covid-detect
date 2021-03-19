from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseForbidden
from django.template import Template,Context
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from cryptography.fernet import Fernet 
from .models import Doctor, Patient, Receptionist, Prescription,Patient_trash

# Create your views here.

def recept_dashboard(request):
    return render(request, "recept_dashboard.html")

def recept_view_doctor(request):
    doctors = Doctor.objects.all()
    con_var = {
        'doctor':doctors
    }
    return render(request, "recept_view_doctor.html",con_var)

def recept_add_doctor(request):
    key = Fernet.generate_key()
    f = Fernet(key)
    if request.method == "POST":
        get_uname=request.POST['uname']
        get_name=request.POST['name']
        get_email=request.POST['email']
        get_password= request.POST['password'].encode()
        print(len(get_password))
        get_address=request.POST['address']
        get_dob=request.POST['dob']
        get_contact=request.POST['contact']
        get_speciality = request.POST['speciality']
        get_gender = request.POST['gender']
        get_blood = request.POST['blood']
        print(get_blood)
        Doctor.objects.create(uname=get_uname, name=get_name,email=get_email,address=get_address, password=get_password, dob=get_dob,contact=get_contact,
        gender=get_gender,speciality=get_speciality,blood=get_blood)
        return render(request, "recept_view_doctor.html")

    else:
        return render(request, "recept_add_doctor.html")

def recept_add_patient(request):
    if request.method == "POST":
        get_name=request.POST['name']
        get_email=request.POST['email']
        get_address=request.POST['address']
        get_dob=request.POST['dob']
        get_contact=request.POST['contact']
        get_gender = request.POST['gender']
        get_blood = request.POST['blood']
        Patient.objects.create(name=get_name,email=get_email,address=get_address,dob=get_dob,contact=get_contact,gender=get_gender,blood=get_blood)
        return HttpResponse("recept_add_patient.html")    
    else:
        return render(request, "recept_add_patient.html")

def recept_view_patient(request):
    patients = Patient.objects.all()
    con_var = {
        'patient':patients
    }
    return render(request, "recept_view_patient.html", con_var)

def doc_dashboard(request):
    return render(request, "doc_dashboard.html")

def doc_add_patient(request):
    if request.method == "POST":
        get_name=request.POST['name']
        get_email=request.POST['email']
        get_address=request.POST['address']
        get_dob=request.POST['dob']
        get_contact=request.POST['contact']
        get_gender = request.POST['gender']
        get_blood = request.POST['blood']
        Patient.objects.create(name=get_name,email=get_email,address=get_address,dob=get_dob,contact=get_contact,gender=get_gender,blood=get_blood)
        return redirect("DocViewPat")   
    else:
        return render(request, "doc_add_patient.html")

def doc_view_patient(request):
    patients = Patient.objects.all()
    con_var = {
        'patient':patients
    }
    return render(request, "doc_view_patient.html",con_var)

def doc_give_prescription(request, ID, name):
    patients = Patient.objects.get(id=ID, name=name)
    prescriptions = Prescription.objects.all()
    con_var = {
        'patient':patients,
        'prescription':prescriptions
    }
    if request.method == "POST":
        get_pid = request.POST['p_id']
        get_name=request.POST['name']
        get_prescription=request.POST['prescription']
        get_date=request.POST['date']
        Prescription.objects.create(p_id=get_pid, name=get_name, prescription=get_prescription,date=get_date)
        return render(request, "doc_give_prescription.html",con_var)    
    else:
        return render(request, "doc_give_prescription.html", con_var)

def doc_delete_patient(request,ID):
    patients = Patient.objects.get(id=ID)
    con_var = {
        'patient': patients
    }
    patients.is_deleted = True
    print(patients.gender)
    Patient_trash.objects.create(name=patients.name,email=patients.email,address=patients.address,dob=patients.dob,
    contact=patients.contact,gender=patients.gender,blood=patients.blood, is_deleted = True)
    patients.delete()
    return render(request, "doc_delete_pat.html", con_var)

