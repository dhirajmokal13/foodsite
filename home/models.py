from tokenize import blank_re
from click import password_option
from django.db import models

# Create your models here.

# This is contact models


class Contact(models.Model):
    name = models.CharField(max_length=122)
    mnumber = models.CharField(max_length=12)
    Comment = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"Id: {self.id} Name: {self.name} Mobile Number: {self.mnumber} Date: {self.date}"


class userlogin(models.Model):
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=12)
    address = models.TextField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    date = models.DateField()


class businesslogin(models.Model):
    oname = models.CharField(max_length=150)
    bname = models.CharField(max_length=150)
    bemail = models.CharField(max_length=100)
    baddr = models.TextField()
    buname = models.CharField(max_length=20)
    bpwd = models.CharField(max_length=20)
    date = models.DateField()


class addplanfood(models.Model):
    pname = models.CharField(max_length=150)
    cpweek = models.IntegerField()
    mealtype = models.CharField(max_length=20)
    buname = models.CharField(max_length=20)
    sunday_meal = models.TextField()
    monday_meal = models.TextField()
    tuesday_meal = models.TextField()
    wednesday_meal = models.TextField()
    thursday_meal = models.TextField()
    friday_meal = models.TextField()
    saturday_meal = models.TextField()
    date = models.DateField()


class bookplane(models.Model):
    name = models.CharField(max_length=150)
    uname = models.CharField(max_length=20)
    buname = models.CharField(max_length=20)
    pid = models.IntegerField()
    pname = models.CharField(max_length=150)
    p_end = models.DateField()
    address = models.TextField()
    no_weeks = models.IntegerField()
    total_amount = models.IntegerField()
    date = models.DateField()

class paymentz(models.Model):
    oid = models.IntegerField()
    amount = models.IntegerField()
    order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)