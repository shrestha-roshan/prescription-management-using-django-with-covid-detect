from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # reception urls
    path('recept/dashboard', recept_dashboard, name= 'recept-dashboard'),
    path('recept/view_doc', recept_view_doctor, name = 'recept-view-doctor'),
    path('recept/add_doc', recept_add_doctor, name= 'recept-add-doctor'),
    path('recept/view_pat',recept_view_patient, name = 'recept-view-patient'),
    path('recept/add_pat', recept_add_patient, name = 'recept-add-patient'),
    path('recept/prescription', recept_prescription, name ='recept-prescription'),
    path('recept/prescription/<int:ID>/<str:name>', recept_view_prescription, name='recept-view-prescription'),

    # doctor urls
    path('doc/dashboard', doc_dashboard, name='doc-dashboard'),
    path('doc/add_pat', doc_add_patient, name= 'doc-add-patient'),
    path('doc/view_pat', doc_view_patient, name='doc-view-patient'),
    path('doc/give_prescription/<int:ID>/<str:name>',doc_give_prescription, name='doc-give-prescription'),
    # path('doc/delete/<int:ID>', patient_trash),
    path('doc/delete/<int:ID>', doc_delete_patient, name='doc-delete-patient'),
    path('doc/prescription/<int:ID>/<str:name>/<int:PID>', doc_delete_prescription, name='doctor-prescription-delete'),
    path('doc/prescription', doc_prescription, name='doc-prescription'),
    
    path('login',login,name='login'),

    path('recept/view_pat/search', recept_search_patient, name='recept-search-patient'),
    path('doc/view_pat/search', doc_search_patient, name='doc-search-patient'),
    path('recept/view_doc/search', recept_search_doctor, name='recept-search-patient'),
    
    path('doc/covid_detect', covid_detect, name = 'covid-detect'),
    path('doc/covid_detect/result', covid_result, name = 'covid-result'),
    # path('doc/covid_detect/test', preictImage, name='predict-image')

    path('recept/update_doc/<int:ID>', recept_update_doc, name='recept-update-doc'),
]