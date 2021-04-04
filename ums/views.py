from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseForbidden
from django.template import Template,Context
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from cryptography.fernet import Fernet 
from .models import Doctor, Patient, Receptionist, Prescription,Patient_trash
from django.db.models import Q
from django.contrib import messages
from keras.models import load_model
from django.core.files.storage import FileSystemStorage
import cv2,os
from keras.preprocessing import image
import numpy as np
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
    doctors = Doctor.objects.all()
    con_var = {
        doctors : 'doctor'
    }
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
        return redirect('recept-view-doctor')
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
        return redirect("doc-view-patient")   
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
    prescriptions = Prescription.objects.filter(p_id=ID)
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

def doc_delete_prescription(request,ID, name, PID):
    prescription = Prescription.objects.get(id=PID)
    prescription.delete()
    return redirect('doc-give-prescription', ID, name)

def recept_prescription(request):
    patients = Patient.objects.all()
    con_var={
        'patient':patients
    }
    return render(request, 'recept_prescription.html',con_var)

def recept_view_prescription(request,ID,name):
    patients = Patient.objects.get(id=ID)
    prescriptions = Prescription.objects.filter(p_id=ID)
    con_var={
        'prescription': prescriptions,
        'patient': patients
    }
    return render(request,'recept_view_prescription.html',con_var)

def doc_prescription(request):
    patients = Patient.objects.all()
    con_var={
        'patient':patients
    }
    return render(request, 'doc_prescription.html',con_var)

def login(request):
    if request.method =="GET":
        return render (request,'login.html')
    else:
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            # login(request,user)
            # return redirect('recept-dashboard')
            if request.POST['login_as'] == 'Doctor':
                match = Doctor.objects.filter(uname__iexact = username, password__iexact = password)
                if match:
                    return redirect('doc-dashboard')
                else:
                    messages.error(request, 'Doctor not registered yet!')
                    return redirect('login')
            elif request.POST['login_as'] == 'Receptionist':
                match = Receptionist.objects.filter(uname__iexact = username, password__iexact = password)
                if match:
                    return redirect('recept-dashboard')
                else:
                    messages.error(request, 'Doctor not registered yet!')
                    return redirect('login')
            else:
                messages.error(request, 'Please specify your login role!')
                return redirect('login')
        else:
            messages.error(request, 'Looks like you leave blank username or password!')
            return redirect('login')

def recept_search_patient(request):
    if request.method=='POST':
        search=request.POST['srh']
        if search:
            match=Patient.objects.filter(Q(name__icontains=search) | Q(dob__icontains = search))
            if match:
                return render(request,'recept_search_patient.html',{'patient':match})
            else:
                messages.error(request, 'Oops! No results Found!')
                return redirect('recept-view-patient')
        else:
            return redirect('recept-view-patient')
    else:
        return redirect('recept-view-patient')

def doc_search_patient(request):
    if request.method=='POST':
        search=request.POST['srh']
        if search:
            match=Patient.objects.filter(Q(name__icontains=search) | Q(dob__icontains = search))
            if match:
                return render(request,'doc_search_patient.html',{'patient':match})
            else:
                messages.error(request, 'Oops! No results Found!')
                return redirect('doc-view-patient')
        else:
            return redirect('doc-view-patient')
    else:
        return redirect('doc-view-patient')

def recept_search_doctor(request):
    if request.method=='POST':
        search=request.POST['srh']
        if search:
            match=Doctor.objects.filter(Q(name__icontains=search) | Q(dob__icontains = search))
            if match:
                return render(request,'recept_search_doc.html',{'doctor':match})
            else:
                messages.success(request, 'Oops! No results Found!')
                return redirect('recept-view-doctor')
        else:
            return redirect('recept-view-doctor')
    else:
        return redirect('recept-view-doctor')

# def predictImage(request):
#     model = load_model(r"C:\Users\user\OneDrive - University of Wolverhampton\fyp\final\model\resnet_covid.h5")
# 	fileObj = request.FILES["uploadfile"]
# 	fs=FileSystemStorage()
# 	filePathName = fs.save(fileObj.name,fileObj)
# 	filePathName = fs.url(filePathName)

# 	test_image = "."+filePathName

# 	img = image.load_img(test_image,target_size=(224,224,3))
# 	img = image.img_to_array(img)
# 	img = img/255
# 	x = img.reshape(1,224,224,3)
# 	# with model_graph.as_default():
# 	# 	with tf_session.as_default():
#     y_pred = resnet.predict(img, workers=0)
#     y_pred = np.where(y_pred>0.70, 'COVID positive','COVID negative')
# 	# prediction = labels[str(np.argmax(proba[0]))]
# 	context={
# 	"filePathName":filePathName,
#     "Predicted" : y_pred
# 	}
# 	return render(request,"test.html",context)


def covid_detect(request):
    return render(request,'covid_detect.html')

def covid_result(request):
    if request.method == 'POST':
        fileObj = request.FILES.get("filename", None)
        fs=FileSystemStorage()
        filePathName = fs.save(fileObj.name,fileObj)
        filePathName = fs.url(filePathName)
        model = load_model(r"C:\Users\user\OneDrive - University of Wolverhampton\fyp\final\model\resnet_covid.h5")


        test_image = "."+filePathName
        print("test_image =",test_image)
        # img = image.load_img(test_image,target_size=(224,224,3))
        # img = np.array(img, dtype='float32')
        # print(img.shape)
        # # img = image.img_to_array(img)
        # img = img/255
        # print(img.shape)

        img = cv2.imread(os.path.join(test_image))
        print("type of image : ",type(img))
        print("path",filePathName)
        print(img.shape)
        img = cv2.resize(img, (224,224))
        img = img.reshape(1,224,224,3)
        print(img.shape)
        img = np.array(img, dtype='float32')
        # with model_graph.as_default():
        # with tf_session.as_default():
        y_pred = model.predict(img, workers=0)
        y_pred = np.where(y_pred>0.70, 'COVID positive','COVID negative')
        # prediction = labels[str(np.argmax(proba[0]))]

        context={
        "filePathName":filePathName,
        "result" : y_pred
        }
        return render(request,"test.html",context)
    else:
        return render(request,"covid-detect.html")

def recept_update_doc(request, ID):
    doctors = Doctor.objects.get(id=ID)
    con_var = {
        'doctor':doctors
    }
    return render(request, 'recept_update_doc.html', con_var)

