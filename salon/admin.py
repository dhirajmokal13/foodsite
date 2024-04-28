from django.contrib import admin
from salon.models import Business, User, Services, Servies_Types, Appointment
# Register your models here.

admin.site.register(Business)
admin.site.register(User)
admin.site.register(Services)
admin.site.register(Servies_Types)
admin.site.register(Appointment)