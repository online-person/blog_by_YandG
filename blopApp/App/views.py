import uuid
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader

from App.models import UserModel, MODIFY_POWER, PostModel, WRITE_POWER
from django.urls import reverse
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
         'uurl':"http://127.0.0.1:8000/blog/activate/{}/".format(token)
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
        data['status'] = 900
    return JsonResponse(data)


def activate(request,token):
    # user_token = request.GET.get('user_token')
    user_id = cache.get(token)

    if not user_id:
        return HttpResponse("激活邮件已过期，请重新申请激活")

    cache.delete(token)

    user = UserModel.objects.get(pk=user_id)

    user.is_act = True
    user.u_authority = MODIFY_POWER
    user.save()

    return HttpResponse('激活成功{}'.format(token))

@csrf_exempt  # 取消csrf验证
def login(request):
    data = {}
    if request.method == "GET":
        data["code"] = 302
        data["message"] = "need a post request"
        return JsonResponse(data)
    else:
        name = request.POST.get("name")
        user = UserModel.objects.filter(u_name=name).first()
        u_pwd = request.POST.get("password")
        if user.verify_pwd(u_pwd):
            data["code"] = 200
            data["message"] = "Login Ok"
            data["user"] = user.u_name
            request.session['user_id'] = user.id
            return JsonResponse(data)
        else:
            data["code"] = 801
            data["message"] = "password error"
            return JsonResponse(data)


def logout(request):
    request.session.flush()
    return JsonResponse({"code":200,"message":"Logout ok"})


def user_info(request):
    user_id = request.session.get("user_id")
    user = UserModel.objects.filter(id=user_id).first()
    user_data = {
        "name":user.u_name,
        "email":user.u_email,
        "icon":str(user.u_icon),
        "auth":user.u_authority,
    }
    return JsonResponse(data=user_data)



@csrf_exempt
def create_post(request):
    if request.method == "POST":
        data = {}
        uid = request.session.get("user_id")
        user = UserModel.objects.filter(id=uid).first()
        if user.u_authority >= WRITE_POWER:
            post = PostModel()
            post.create_post(user,request.POST)
            data["code"] = 200
            data["message"] = "create post ok"
            return JsonResponse(data)
        data["code"] = 403
        data["message"] = "you has not authority!"
        return JsonResponse(data)



def del_post(request,pid):
    data = {}
    post = PostModel.objects.filter(id=pid).filter(is_del=False).first()
    if post == None:
        data["code"] = 404
        data["message"] = "post does not exist!"
        return JsonResponse(data)

    data["message"],data["code"] = post.deleted(request) or ("del post ok",200)
    return JsonResponse(data)

@csrf_exempt
def modify_post(request,pid):
    if request.method == "POST":
        data = {}
        post = PostModel.objects.filter(id=pid).filter(is_del=False).first()
        if post == None:
            data["code"] = 404
            data["message"] = "post doesn't exist!"
            return JsonResponse(data)

        data["message"],data["code"] = post.modify(request) or ("modify ok",200)

        return JsonResponse(data)


def recovery_post(request,pid):
    data = {}
    post = PostModel.objects.filter(id=pid).filter(is_del=True).first()
    if post == None:
        data["code"] = 404
        data["message"] = "post does not exist!"
        return JsonResponse(data)

    data["message"], data["code"] = post.recovery(request) or ("recovery post ok", 200)
    return JsonResponse(data)


def post_info(request,pid):
    data = {}
    post = PostModel.objects.filter(id=pid).filter(is_del=False).first()
    if post == None:
        data["code"] = 404
        data["message"] = "post doesn't exist!"
        return JsonResponse(data)
    data = post.toDict()
    data["code"] = 200
    return JsonResponse(data=data)



def post_list(request,page=1,items=10):
    start = (int(page)-1)*10
    end = start + int(items)
    posts = PostModel.objects.filter(is_del=False).order_by("-p_update")[start:end]
    data = {}
    for post in iter(posts):
        data[post.id] = post.toDict()
    data["code"] = 200
    return JsonResponse(data=data)