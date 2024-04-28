from django.shortcuts import render, HttpResponse, redirect
from salon.models import Business, User, Services, Servies_Types, Appointment
from django.contrib import messages
from salon.utils import business_login_required, user_login_required
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.


def index(req):
    # check is this search for service
    if req.GET.get('search_txt', None) and not req.GET.get('search_txt', None) == '':
        search_query = req.GET.get('search_txt', None)
        business_services_all = Servies_Types.objects.select_related('business', 'services').filter(
            Q(service_type_name__icontains=search_query) | Q(services__service_name__icontains=search_query) | Q(gender__icontains=search_query) | Q(business__salon_name__icontains=search_query))
        return render(req, 'salon/search.html', {'session': req.session, 'business_services': business_services_all})
    services = Services.objects.all()
    business_services_all = Servies_Types.objects.select_related(
        'business', 'services').all()
    return render(req, 'salon/index.html', {'session': req.session, 'Services': services, 'business_services': business_services_all})


@business_login_required
def business_services(req):
    if req.method == 'POST' and req.POST.get('service_add'):
        service_name = req.POST.get('service_name')
        if Servies_Types.objects.filter(service_type_name=service_name, services_id=req.session['user']['id']).exists():
            messages.error(req, "Duplicate Service")
            return redirect("business/services/")
        business = Business.objects.get(id=req.session['user']['id'])
        service = Services.objects.get(id=req.POST.get('service_id'))
        Servies_Types.objects.create(
            service_type_name=service_name,
            service_image=req.FILES['service_image'],
            service_cost=req.POST.get('service_cost'),
            gender=req.POST.get('gender'),
            business=business,
            services=service,
            description=req.POST.get('service_desc')
        )
        messages.success(req, "Service Added Successfully")
        return redirect("/salon/business/services")
    services = Services.objects.all()
    business_services_my = Servies_Types.objects.select_related(
        'business', 'services').filter(business_id=req.session['user']['id'])
    return render(req, 'salon/business/services.html', {'session': req.session, 'Services': services, 'business_services': business_services_my})


@business_login_required
def remove_business_service(req, service_id):
    try:
        Servies_Types.objects.filter(
            id=service_id,
            business_id=req.session['user']['id']
        ).delete()
        messages.success(req, "Service Removed Successfully")
    except:
        messages.error(req, "Something went to wrong")

    return redirect("/salon/business/services")


@business_login_required
def get_business_appointments(req):
    appointment = Appointment.objects.select_related('service__services', 'customer').filter(
        service__business_id=req.session['user']['id']).order_by('-appointment_creation_date')
    return render(req, "salon/business/appointments.html", {'session': req.session, 'appointments': appointment})


@user_login_required
def get_user_appointments(req):
    appointment = Appointment.objects.select_related('service__services', 'service__business').filter(
        customer_id=req.session['user']['id']).order_by('-appointment_creation_date')
    return render(req, "salon/user/my_appointments.html", {'session': req.session, 'appointments': appointment})


@business_login_required
def complete_business_appointment(req, appointment_id):
    try:
        Appointment.objects.filter(
            id=appointment_id,
            service__business_id=req.session['user']['id']
        ).update(
            appointment_status='completed'
        )
        messages.success(req, "Appointment Completed")
    except:
        messages.error(req, "something went wrong")
    return redirect("/salon/business/appointments")


@user_login_required
def cancel_user_appointment(req):
    if req.method == 'POST' and req.POST.get('appointment_cancel_btn'):
        try:
            Appointment.objects.filter(
                id=req.POST.get('appointment_id'),
                customer_id=req.session['user']['id']
            ).update(
                appointment_status='cancel',
                appointment_cancellation_reason=f"user: {req.POST.get('appointment_cancellation_reason')}"
            )
            messages.success(req, "Appointment Cancelled")
        except Exception as e:
            print(e)
            messages.error(req, "Something went wrong")
    return redirect("/salon/user/appointments")


@business_login_required
def cancel_business_appointment(req):
    if req.method == 'POST' and req.POST.get('appointment_cancel_btn'):
        try:
            Appointment.objects.filter(
                id=req.POST.get('appointment_id'),
                service__business_id=req.session['user']['id']
            ).update(
                appointment_status='cancel',
                appointment_cancellation_reason=f"Business: {req.POST.get('appointment_cancellation_reason')}"
            )
            messages.success(req, "Appointment Cancelled")
        except:
            messages.error(req, "Something went wrong")
    return redirect("/salon/business/appointments")


@user_login_required
def book_appointment(req, service_id):
    if req.method == 'POST' and req.POST.get('appointment_confirm'):
        customer = User.objects.get(id=req.session['user']['id'])
        service = Servies_Types.objects.get(id=service_id)
        Appointment(
            customer=customer,
            service=service,
            appointment_date=req.POST.get('appointment_date'),
            appointment_start_time=req.POST.get('appointment_time')
        ).save()
        messages.success(req, "Appointment Booked Successfully")
        return redirect("/salon")
    selected_service = Servies_Types.objects.select_related(
        'business', 'services').filter(id=service_id).first()
    return render(req, "salon/user/appointment.html", {'session': req.session, 'selected_service': selected_service})


def get_available_appointment(req, business_id, date):
    return JsonResponse({'data': Business.objects.get(id=business_id).get_available_appointment(date)})


def business_register(req):
    if req.method == 'POST' and req.POST.get('businessSignup'):
        salon_name = req.POST.get('name')
        salon_email = req.POST.get('email')
        password = req.POST.get('password')
        address = req.POST.get('address')
        open_time = req.POST.get('open_time')
        closing_time = req.POST.get('close_time')
        owner = req.POST.get('owner')
        profile = req.FILES['profile']
        exist = Business.objects.filter(salon_email=salon_email).exists()
        if not exist:
            try:
                Business(
                    salon_owner_name=owner,
                    salon_name=salon_name,
                    salon_email=salon_email,
                    salon_address=address,
                    salon_profile_pic=profile,
                    open_time=open_time,
                    closing_time=closing_time,
                    password=password
                ).save()
                messages.success(req, "Account Created Successfully")
            except:
                messages.error(req, "Something went wrong")
            return redirect('/salon')
        messages.error(req, "Email Already Registered")
        return redirect('/salon')
    messages.error(req, "Invalid Method")
    return redirect('/salon')


def user_register(req):
    if req.method == 'POST' and req.POST.get('userSignup'):
        user_name = req.POST.get('name')
        user_email = req.POST.get('email')
        user_mobile = req.POST.get('mobile')
        profile = req.FILES['profile']
        password = req.POST.get('password')
        exist = User.objects.filter(user_email=user_email).exists()
        if not exist:
            try:
                User(
                    user_name=user_name,
                    user_email=user_email,
                    user_mobile=user_mobile,
                    user_profile_pic=profile,
                    password=password
                ).save()
                messages.success(req, "Account Created Successfully")
            except:
                messages.error(req, "Something went wrong")
            return redirect('/salon')
        messages.error(req, "Email Already Registered")
        return redirect('/salon')
    messages.error(req, "Invalid Method")
    return redirect('/salon')


def business_login(req):
    if req.method == 'POST' and req.POST.get('business_login'):
        email = req.POST.get('email')
        password = req.POST.get('password')
        try:
            exist = Business.objects.get(salon_email=email)
            if (exist.validate_password(password)):
                req.session['loggedIn'] = True
                req.session['type_of_loggedin'] = "Business"
                req.session['user'] = {
                    'id': exist.id,
                    'salon_name': exist.salon_name,
                    'salon_email': exist.salon_email,
                    'salon_location': exist.get_location(),
                    'salon_profile': exist.salon_profile_pic.name
                }
                messages.success(req, "Login Success")
                return redirect("/salon")
            messages.error(req, "Invalid Credentials")
        except:
            messages.error(req, "Invalid Credentials")
        return redirect("/salon")
    return render(req, 'salon/business/login_signup.html', {'session': req.session})


def user_login(req):
    if req.method == 'POST' and req.POST.get('user_login'):
        email = req.POST.get('email')
        password = req.POST.get('password')
        try:
            exist = User.objects.get(user_email=email)
            if (exist.validate_password(password)):
                req.session['loggedIn'] = True
                req.session['type_of_loggedin'] = "user"
                req.session['user'] = {
                    'id': exist.id,
                    'user_email': exist.user_email,
                    'user_mobile': exist.user_mobile,
                    'user_profile': exist.user_profile_pic.name
                }
                messages.success(req, "Login Success")
                return redirect("/salon")
        except:
            messages.error(req, "Invalid Credentials")
        return redirect("/salon")
    return render(req, 'salon/user/login_signup.html', {'session': req.session})


def Signout(req):
    req.session['loggedIn'] = False
    req.session['type_of_loggedin'] = ""
    req.session['user'] = {}
    messages.success(req, 'Logout successfully')
    return redirect("/salon")
