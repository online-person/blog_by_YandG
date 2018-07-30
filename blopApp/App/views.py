import uuid
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from App.models import UserModel, MODIFY_POWER, PostModel
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("hello world")


@csrf_exempt
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
    send_mail(
         'Subject {}'.format(uname),
         '',
         '16601156043@163.com',
         [ucemail,],
         html_message = html_mes,
     )

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
    user.u_authority = MODIFY_POWER
    user.save()

    return HttpResponse('激活成功{}'.format(user_token))

@csrf_exempt  # 取消csrf验证
def login(request):
    if request.method == "GET":
        print("-------------")
        return HttpResponse("login")
    else:
        name = request.POST.get("name")
        user = UserModel.objects.filter(u_name=name).first()
        u_pwd = request.POST.get("password")
        if user.verify_pwd(u_pwd):

            request.session['user_id'] = user.id
            return HttpResponse("login ok")
        else:
            return HttpResponse("密码 错误")


def logout(request):
    request.session.flush()
    return HttpResponse("退出成功")


def user_info(request):
    user_id = request.session.get("user_id")
    user = UserModel.objects.filter(id=user_id).first()
    user_data = {
        "name":user.u_name,
        "email":user.u_email,
        "icon":str(user.u_icon),
    }
    return JsonResponse(data=user_data)

