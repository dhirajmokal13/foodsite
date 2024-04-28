from django.contrib import admin
from django.urls import path
from salon import views

urlpatterns = [
    path("", views.index, name='home'),
    path("business/login/", views.business_login, name='business_login'),
    path("user/login/", views.user_login, name="user_login"),
    path("user/service/appointment/<int:service_id>", views.book_appointment, name="book_appointment"),
    path("business/signup/", views.business_register, name='business_register'),
    path("business/services/", views.business_services, name="business_services"),
    path("business/appointments", views.get_business_appointments, name="business_appointments"),
    path("user/appointments", views.get_user_appointments, name="user_appointments"),
    path("business/appointment/complete/<int:appointment_id>", views.complete_business_appointment, name="business_appoinment_complete"),
    path("business/appointment/cancel", views.cancel_business_appointment, name="cancel_business_appointment"),
    path("user/appointment/cancel", views.cancel_user_appointment, name="cancel_user_appointment"),
    path("business/appointment/check/<int:business_id>/<str:date>", views.get_available_appointment, name="appointment_available"),
    path("business/service/remove/<int:service_id>", views.remove_business_service, name="remove_business_service"),
    path("user/signup/", views.user_register, name='user_register'),
    path("logout", views.Signout, name="logout")
]