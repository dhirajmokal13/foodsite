from numpy import ogrid
import razorpay
from click import password_option
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, date, timedelta
from home.models import Contact, userlogin, businesslogin, addplanfood, bookplane, paymentz
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# some import functions


def pwdcnf(x, y):
    if x == y:
        return True
    else:
        return False


def checkUserName(username):
    try:
        userlogin.objects.get(username=username)
        return True
    except Exception:
        return False


def checkBUname(username):
    try:
        businesslogin.objects.get(buname=username)
        return True
    except Exception:
        return False


def index(request):
    plan = addplanfood.objects.all()
    data = {
        'session': request.session,
        'plan': plan,
    }
    return render(request, 'index.html', data)


def bookplan(request, id):
    if request.session.get('userlogin') != True:
        return redirect(userLogin)
    plan = addplanfood.objects.filter(id=id)
    nw = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
          12, 13, 14, 15, 16, 17, 18, 19, 20]
    data = {
        'id': id,
        'session': request.session,
        'plan': plan,
        'nw': nw,
    }
    if request.method == 'POST' and request.POST.get('cnfbooking') == 'true':
        buname = plan[0].buname
        amount = plan[0].cpweek
        pname = plan[0].pname
        name = request.session.get('name')
        uname = request.session.get('username')
        addr = request.POST.get('address')
        no_week = request.POST.get('nofw')
        p_end = str(date.today() + timedelta(weeks=int(no_week)))
        total_amount = int(amount) * int(no_week)
        result = bookplane(name=name, uname=uname, buname=buname, pid=id, pname=pname, p_end=p_end, address=addr, no_weeks=no_week,
                           total_amount=total_amount, date=datetime.today())
        result.save()
        global oid 
        oid = result.id
        return redirect(checkout)
    return render(request, 'user/bookplan.html', data)


@csrf_exempt
def payment_status(request):
    res = request.POST
    status = None
    client = razorpay.Client(
        auth=('rzp_test_V8dibsyOXL32Hd', 'zlfqXvcm3WJhmnh8PzugAjcB'))
    try:
        client.utility.verify_payment_signature(
            {'razorpay_order_id': res['razorpay_order_id'], 'razorpay_payment_id': res['razorpay_payment_id'], 'razorpay_signature': res['razorpay_signature']})
        paymentz.objects.filter(order_id=res['razorpay_order_id']).update(
            razorpay_payment_id=res['razorpay_payment_id'], paid=True)
        status = True
    except Exception:
        status = False
    data = {
        'session': request.session,
        'status':status,
    }
    return render(request, 'payments/payment-status.html', data)


def checkout(request):
    # payment gateway start here
    order = bookplane.objects.get(id=oid)
    user = userlogin.objects.get(username=order.uname)
    order_amount = "200"  # order.total_amount * 100
    order_currency = 'INR'
    try:
        client = razorpay.Client(
            auth=('rzp_test_V8dibsyOXL32Hd', 'zlfqXvcm3WJhmnh8PzugAjcB'))
        payment = client.order.create(
            {'amount': order_amount, 'currency': 'INR', 'payment_capture': '1'})
    except Exception:
        return HttpResponse("Something went to wrong Check Internet")
    order_id = payment['id']
    order_status = payment['status']
    if order_status == 'created':
        result = paymentz(oid=oid, amount=int(order_amount)/100, order_id=order_id)
        result.save()
        # payment gateway end here
        data = {
            'oid': oid,
            'session': request.session,
            'payment': payment,
            'name': order.name,
        }
        return render(request, 'payments/checkout.html', data)


def about(request):
    data = {
        'session': request.session,
    }
    return render(request, 'about.html', data)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('cname')
        mnumber = request.POST.get('mnumber')
        comment = request.POST.get('comment')
        contact = Contact(name=name, mnumber=mnumber,
                          Comment=comment, date=datetime.today())
        result = contact.save()
        print(result)
        messages.success(request, 'Contact Submitted successfully')
    data = {
        'session': request.session,
    }
    return render(request, 'contact.html', data)


def addplan(request):
    if request.session.get('businesslogin') != True:
        return redirect(businessLogin)
    data = {
        'session': request.session,
    }
    if request.method == 'POST' and request.POST.get('plansub') == 'true':
        pname = request.POST.get('pname')
        cpweek = request.POST.get('cpweek')
        mealtype = request.POST.get('mealtype')
        sunday_meal = f"{request.POST.get('sbf')}:::{request.POST.get('slunch')}:::{request.POST.get('sdinner')}"
        monday_meal = f"{request.POST.get('mbf')}:::{request.POST.get('mlunch')}:::{request.POST.get('mdinner')}"
        tuesday_meal = f"{request.POST.get('tbf')}:::{request.POST.get('tlunch')}:::{request.POST.get('tdinner')}"
        wednesday_meal = f"{request.POST.get('wbf')}:::{request.POST.get('wlunch')}:::{request.POST.get('wdinner')}"
        thursday_meal = f"{request.POST.get('thbf')}:::{request.POST.get('thlunch')}:::{request.POST.get('thdinner')}"
        friday_meal = f"{request.POST.get('fbf')}:::{request.POST.get('flunch')}:::{request.POST.get('fdinner')}"
        saturday_meal = f"{request.POST.get('stbf')}:::{request.POST.get('stlunch')}:::{request.POST.get('stdinner')}"
        buname = request.session.get('buname')
        result = addplanfood(pname=pname, cpweek=cpweek, mealtype=mealtype, buname=buname,
                             sunday_meal=sunday_meal, monday_meal=monday_meal, tuesday_meal=tuesday_meal, wednesday_meal=wednesday_meal, thursday_meal=thursday_meal, friday_meal=friday_meal, saturday_meal=saturday_meal, date=datetime.today()).save()
    return render(request, 'panels/addplan.html', data)


def planlist(request):
    if request.session.get('businesslogin') != True:
        return redirect(businessLogin)
    plan_data = addplanfood.objects.filter(
        buname=request.session.get('buname'))
    data = {
        'session': request.session,
        'food_plans': plan_data,
    }
    return render(request, 'panels/planlist.html', data)


def delplan(request, id):
    if request.session.get('businesslogin') != True:
        return redirect(businessLogin)
    try:
        result = addplanfood.objects.get(
            id=id, buname=request.session.get('buname')).delete()
        print(result)
        return redirect(planlist)
    except Exception:
        return HttpResponse("Somthing is not Right")


def updateplan(request, id):
    if request.session.get('businesslogin') != True:
        return redirect(businessLogin)
    datas = addplanfood.objects.filter(
        id=id, buname=request.session.get('buname'))
    data = {
        'session': request.session,
        'id': id,
        'datas': datas,
    }
    if request.method == 'POST' and request.POST.get('planupdate') == 'true':
        pname = request.POST.get('pname')
        cpweek = request.POST.get('cpweek')
        mealtype = request.POST.get('mealtype')
        sunday_meal = f"{request.POST.get('sbf')}:::{request.POST.get('slunch')}:::{request.POST.get('sdinner')}"
        monday_meal = f"{request.POST.get('mbf')}:::{request.POST.get('mlunch')}:::{request.POST.get('mdinner')}"
        tuesday_meal = f"{request.POST.get('tbf')}:::{request.POST.get('tlunch')}:::{request.POST.get('tdinner')}"
        wednesday_meal = f"{request.POST.get('wbf')}:::{request.POST.get('wlunch')}:::{request.POST.get('wdinner')}"
        thursday_meal = f"{request.POST.get('thbf')}:::{request.POST.get('thlunch')}:::{request.POST.get('thdinner')}"
        friday_meal = f"{request.POST.get('fbf')}:::{request.POST.get('flunch')}:::{request.POST.get('fdinner')}"
        saturday_meal = f"{request.POST.get('stbf')}:::{request.POST.get('stlunch')}:::{request.POST.get('stdinner')}"
        buname = request.session.get('buname')
        addplanfood.objects.filter(id=id, buname=buname).update(pname=pname, cpweek=cpweek, mealtype=mealtype, sunday_meal=sunday_meal, monday_meal=monday_meal,
                                                                tuesday_meal=tuesday_meal, wednesday_meal=wednesday_meal, thursday_meal=thursday_meal, friday_meal=friday_meal, saturday_meal=saturday_meal)
        messages.success(request, 'Plan Updated Successfully')
        return redirect(planlist)
    return render(request, 'panels/updateplan.html', data)


def showorders(request):
    if request.session.get('businesslogin') != True:
        return redirect(businessLogin)
    buname = request.session.get('buname')
    orders = bookplane.objects.filter(buname=buname)
    data = {
        'session': request.session,
        'orders': orders,
    }
    return render(request, 'panels/showorders.html', data)


def myorders(request):
    if request.session.get('userlogin') != True:
        return redirect(userLogin)
    uname = request.session.get('username')
    orders = bookplane.objects.filter(uname=uname)
    data = {
        'session': request.session,
        'orders': orders,
    }
    return render(request, 'user/myorders.html', data)


# login data start here


def logout(request):
    request.session.clear()
    messages.success(request, 'Successfully Logged Out')
    return redirect(index)


def usersignup(request):
    if request.session.get('userlogin') == True or request.session.get('businesslogin') == True:
        return redirect(index)
    if request.method == 'POST':
        if request.POST.get('userreg'):
            if pwdcnf(request.POST.get('pwd'), request.POST.get('cpwd')) == True:
                if checkUserName(request.POST.get('username')) == False:
                    name = request.POST.get('name')
                    mobile = request.POST.get('mobile')
                    addr = request.POST.get('addr')
                    username = request.POST.get('username')
                    pwd = make_password(request.POST.get('pwd'))
                    data = userlogin(name=name, mobile=mobile, address=addr,
                                     username=username, password=pwd, date=datetime.today())
                    result = data.save()
                    messages.success(request, 'Account Created Successfully')
                else:
                    messages.error(request, 'Username is already Registered')
            else:
                messages.error(request, 'Password did not match')
    data = {
        'session': request.session,
    }
    return render(request, 'logins/usersignup.html', data)


def businessLogin(request):
    if request.session.get('userlogin') == True or request.session.get('businesslogin') == True:
        return redirect(index)
    if request.method == 'POST' and request.POST.get('bjnlgn') == 'true':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        try:
            user = businesslogin.objects.get(buname=username)
            if check_password(password, user.bpwd):
                request.session['businesslogin'] = True
                request.session['buname'] = user.buname
                return redirect(index)
            else:
                messages.error(request, "Invalid Credentials")
        except Exception as err:
            messages.error(request, "Invalid Credentials")

    data = {
        'session': request.session,
    }
    return render(request, 'logins/businessLogin.html', data)


def userLogin(request):
    if request.session.get('userlogin') == True or request.session.get('businesslogin') == True:
        return redirect(index)
    if request.method == 'POST' and request.POST.get('usrlgn') == 'true':
        username = request.POST.get('uname')
        password = request.POST.get('password')
        try:
            user = userlogin.objects.get(username=username)
            if check_password(password, user.password):
                request.session['username'] = user.username
                request.session['address'] = user.address
                request.session['name'] = user.name
                request.session['userlogin'] = True
                return redirect(index)
            else:
                messages.error(request, "Invalid Credentials")
        except Exception as err:
            messages.error(request, "Invalid Credentials")
    data = {
        'session': request.session,
    }
    return render(request, 'logins/userLogin.html', data)


def businesssignup(request):
    if request.session.get('userlogin') == True or request.session.get('businesslogin') == True:
        return redirect(index)
    if request.method == 'POST' and request.POST.get('bjnsignup'):
        if pwdcnf(request.POST.get('bpwd'), request.POST.get('cbpwd')) == True:
            if checkBUname(request.POST.get('username')) == False:
                oname = request.POST.get('boname')
                bname = request.POST.get('bname')
                bemail = request.POST.get('bemail')
                baddr = request.POST.get('baddr')
                buname = request.POST.get('buname')
                bpwd = make_password(request.POST.get('bpwd'))
                data = businesslogin(oname=oname, bname=bname, bemail=bemail,
                                     baddr=baddr, buname=buname, bpwd=bpwd, date=datetime.today())
                result = data.save()
                messages.success(request, 'Account Created Successfully')
            else:
                messages.error(request, 'Username is already Registered')
        else:
            messages.error(request, 'Password did not match')
    data = {
        'session': request.session,
    }
    return render(request, "logins/businesssignup.html", data)

# Login end here
