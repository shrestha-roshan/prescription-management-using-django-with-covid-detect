from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # reception urls
    path('recept/dashboard', recept_dashboard, name= 'recept-dashboard'),
    path('recept/view_doc', recept_view_doctor, name = 'recept-view-doctor'),
    path('recept/add_doc', recept_add_doctor, name= ' recept-add-doctor'),
    path('recept/view_pat',recept_view_patient, name = 'recept-view-patient'),
    path('recept/add_pat', recept_add_patient, name = 'recept-add-patient'),

    # doctor urls
    path('doc/dashboard', doc_dashboard, name='doc-dashboard'),
    path('doc/add_pat', doc_add_patient, name= 'doc-add-patient'),
    path('doc/view_pat', doc_view_patient, name='doc-view-patient'),
    path('doc/give_prescription/<int:ID>/<str:name>',doc_give_prescription, name='doc-give-prescription'),
    # path('doc/delete/<int:ID>', patient_trash),
    path('doc/delete/<int:ID>', doc_delete_patient, name='doc-delete')
]