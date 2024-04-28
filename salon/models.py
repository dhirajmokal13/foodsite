from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime
from salon.utils import get_today_date


class Business(models.Model):
    salon_owner_name = models.CharField(max_length=60)
    salon_name = models.CharField(max_length=40)
    salon_email = models.EmailField(max_length=40, unique=True)
    salon_location = models.CharField(
        max_length=100, default=None, blank=True, null=True)
    salon_address = models.CharField(max_length=150, default='')
    salon_profile_pic = models.ImageField(
        max_length=255, default='', upload_to='business/profile')
    open_time = models.TimeField(default=None, blank=True, null=True)
    closing_time = models.TimeField(default=None, blank=True, null=True)
    password = models.TextField()

    # it will hash the password before save to database
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # it will check the password correctness
    def validate_password(self, pwd):
        return check_password(pwd, self.password)

    # get the location from database
    def get_location(self):
        if self.salon_location and len(self.salon_location) > 1:
            self.salon_location = list((self.salon_location).split(":"))
        return self.salon_location
    
    def _generate_time_intervals(self, start_time, end_time, interval_minutes):
        current_time = datetime.datetime.combine(
            datetime.date.today(), start_time)
        end_datetime = datetime.datetime.combine(
            datetime.date.today(), end_time)
        while current_time < end_datetime:
            yield current_time.strftime('%H:%M:%S')
            current_time += datetime.timedelta(minutes=interval_minutes)

    def get_available_appointment(self, date):
        appointment = []
        appoint = Appointment.objects.select_related('service__business').filter(service__business_id=self.id, appointment_date=date)
        times = list(self._generate_time_intervals(self.open_time, self.closing_time, 30))
        appointment = [str(single_appointment.appointment_start_time) for single_appointment in appoint]
        return [element for element in times if element not in appointment]


class User(models.Model):
    user_name = models.CharField(max_length=40)
    user_email = models.EmailField(max_length=40, unique=True)
    user_mobile = models.IntegerField()
    user_profile_pic = models.ImageField(
        max_length=255, default='', upload_to='user/profile')
    password = models.TextField()

    # it will hash the password before save to database
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # it will check the password correctness
    def validate_password(self, pwd):
        return check_password(pwd, self.password)


class Services(models.Model):
    service_name = models.CharField(max_length=100, unique=True)
    service_icon = models.ImageField(
        max_length=255, default='', upload_to='service/icon')


class Servies_Types(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    BOTH = 'both'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (BOTH, 'Both'),
    ]

    service_type_name = models.CharField(max_length=100)
    service_image = models.ImageField(
        max_length=255, default='', upload_to='service/image')
    # this means for whom this service is available
    service_cost = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)
    description = models.TextField(default='')

    class Meta:
        unique_together = ['service_type_name', 'business']


class Appointment(models.Model):
    CONFIRMATION = [
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('cancel', 'cancel')
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Servies_Types, on_delete=models.CASCADE)
    appointment_status = models.CharField(
        max_length=10, choices=CONFIRMATION, default='pending')
    appointment_date = models.DateField()
    appointment_creation_date = models.DateField(default=get_today_date)
    appointment_start_time = models.TimeField()
    appointment_end_time = models.TimeField()
    appointment_cancellation_reason = models.TextField(
        default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.appointment_start_time:
            self.appointment_end_time =  datetime.timedelta(minutes=30) + datetime.datetime.strptime(self.appointment_start_time, '%H:%M:%S')
        super().save(*args, **kwargs)

