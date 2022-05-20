from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("logout", views.logout, name='Logout'),
    path("addplan", views.addplan, name='addplan'),
    path("planlist", views.planlist, name='planlist'),
    path("showorders", views.showorders, name='showorders'),
    path("myorders", views.myorders, name='myorders'),
    path("checkout", views.checkout, name='checkout'),
    path("payment-status", views.payment_status, name='payment-status'),
    path("bookplan/<int:id>", views.bookplan, name='bookpanel'),
    path('delplan/<int:id>', views.delplan, name='delplan'),
    path('updateplan/<int:id>', views.updateplan, name='updateplan'),
    path("usersignup", views.usersignup, name='usersignup'),
    path("userLogin", views.userLogin, name='userLogin'),
    path("businessLogin", views.businessLogin, name='BuinessLogin'),
    path("businesssignup", views.businesssignup, name='BusinessSignup'),
]