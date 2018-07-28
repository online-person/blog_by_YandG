import uuid
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from App.models import UserModel, DEL_SELF_POWER


def index(request):
    return HttpResponse("hello world")

def user_register(request):
    if request.method == "GET":
        data = {
            'title': '注册'
        }
        return render(request, 'user/user_regis.html', context=data)

    elif request.method == "POST":
        u_name = request.POST.get('user_Name')
        u_email = request.POST.get('user_Email')
        u_pwd = request.POST.get('user_Password')
        u_icon = request.FILES.get('user_Icon')

        user = UserModel()
        user.u_name = u_name
        user.set_pwd(u_pwd)
        user.u_icon = u_icon
        user.u_email = u_email
        user.save()
        request.session["user_id"] = user.id

        token = str(uuid.uuid4())

        cache.set(token,user.id,timeout=60*60)

        send_email_test(u_name, u_email, token)

        return HttpResponse("register ok")

def send_email_test(uname,ucemail,token):
    temp = loader.get_template('user/activate.html')
    data = {
         'uname':uname,
         'uurl':"http://127.0.0.1/blog/activate/?user_token={}".format(token)
     }
    html_mes = temp.render(data)
    print("---------------------------------------")
    send_mail(
         'Subject {}'.format(uname),
         '',
         '16601156043@163.com',
         [ucemail,],
         html_message = html_mes,
     )
    print("---------------------------------------")

def check_name(request):
    u_name = request.GET.get('u_name')
    user = UserModel.objects.filter(u_name=u_name)
    data = {'mesg':'ok',
            'status':'200'}
    if user.exists():
        data['mesg'] = 'not aviable'
        data['status'] = '900'
    return JsonResponse(data)


def activate(request):
    user_token = request.GET.get('user_token')
    user_id = cache.get(user_token)

    if not user_id:
        return HttpResponse("激活邮件已过期，请重新申请激活")

    cache.delete(user_token)

    user = UserModel.objects.get(pk=user_id)

    user.isactive = True
    user.u_authority = DEL_SELF_POWER
    user.save()

    return HttpResponse('激活成功{}'.format(user_token))