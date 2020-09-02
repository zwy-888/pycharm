import hashlib
import random
import string
import uuid


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import settings
from userapp.captcha.image import ImageCaptcha
from userapp.models import User


def register(request):
    return render(request, 'user/register.html')

def register_logic(request):
    print('注册业务逻辑')
    cap_code = request.POST.get('captcha')
    if cap_code.lower() != request.session.get('code').lower():
        print(1111111)
        return JsonResponse({'msg': '验证码有误', 'status': 0})
    # 3. 注册
    user_name = request.POST.get("user_name")
    pwd = request.POST.get("pwd")
    email = request.POST.get("email")
    # 加盐
    salt = str(uuid.uuid4)
    pwd2 = pwd + salt
    # 加密
    sha = hashlib.sha256()
    sha.update(pwd2.encode())
    password = sha.hexdigest()
    print(password)

    try:
        with transaction.atomic():
            user = User.objects.create(name=user_name, password=password, email=email,salt=salt)
            if user:
                ser = Serializer(settings.SECRET_KEY, expires_in=240)  # 声明一个对象
                token = ser.dumps({'id': user.id})  # 加密后的令牌 返回值为bytes
                token = token.decode('utf-8')  # 转为字符串
                send_mail('帐户激活',
                          'http://127.0.0.1:8000/userapp/active/?token=' + token, '2970920254@qq.com',
                          ['2970920254@qq.com'],
                          fail_silently=False)
            return JsonResponse({'msg': '注册成功', 'status': 1})
    except:
        return JsonResponse({'msg': '注册失败', 'status': 0})

        # if user:
            #     ser = Serializer(settings.SECRET_KEY, expires_in=240)  # 声明一个对象
            #     token = ser.dumps({'id': user.id})  # 加密后的令牌 返回值为bytes
            #     token = token.decode('utf-8')  # 转为字符串
            #     send_mail('帐户激活', 'http://127.0.0.1:8000/userapp/active/?token='+token, '2970920254@qq.com',
            #               ['2970920254@qq.com'], fail_silently=False)
    #             return JsonResponse({'msg': '注册成功', 'status': 1})
    #         else:
    #             return JsonResponse({'msg': '邮件发送是失败', 'status': 0})
    # except:
    #     JsonResponse({'msg': '注册失败', 'status': 0})


def active(request):
    try:
        rst = request.GET.get('token')
        # 进行解密
        print(rst)
        ser = Serializer(settings.SECRET_KEY, expires_in=240)
        rst_dict = ser.loads(rst)
        id = rst_dict.get('id')
        user = User.objects.get(pk=id)
        print(user)
        if user.active:
            return HttpResponse('恭喜' + user.name + '账户已经审核过了')
        user.active = True
        user.save()
        return HttpResponse('恭喜' + user.name + '账户被成功激活快去登录吧')
    except SignatureExpired as s:
        return HttpResponse('不好意思，链接已经失效！')
    except:
        return HttpResponse('对不起，激活失败')


def login(request):
    return render(request, 'user/login.html')


def login_logic(request):
    name = request.POST.get('username')
    print(name)
    pwd = request.POST.get('pwd')
    # cookie是记住我
    cookie = request.POST.get('cookie')
    rst = User.objects.filter(name=name)

    # rst = User.objects.filter(name=name)
    sha = hashlib.sha256()
    print(rst)
    # if rst:
    salt = rst[0].salt  #获取后端的盐
    sha.update((pwd + salt).encode())# 对前端获取的数据加盐在加密在encode
    pwd = sha.hexdigest() # 密文
    print(pwd)
    if rst[0].password == pwd:

        if rst[0].active:
            res = JsonResponse({'msg': 'ok', 'status': 1})
            if cookie:
                res.set_cookie('username', name, max_age=7 * 24 * 3600)
                res.set_cookie('userpwd', pwd, max_age=7 * 24 * 3600)
            return res
        else:
            ser = Serializer(settings.SECRET_KEY, expires_in=240)  # 声明一个对象
            token = ser.dumps({'id': rst[0].id})  # 加密后的令牌 返回值为bytes
            token = token.decode('utf-8')  # 转为字符串
            send_mail('帐户激活',
                      'http://127.0.0.1:8000/userapp/active/?token=' + token, '2970920254@qq.com', ['2970920254@qq.com'],
                      fail_silently=False)
            return JsonResponse({'msg': '账号未激活', 'status': 2})
    else:
        return JsonResponse({'msg': '用户名或密码输入不正确', 'status': 0})

    #                 if user.active:# 修改数据库is_active字段
    #                     res = JsonResponse({'msg': 'ok', 'status': 1})
    #                     if cookie:
    #                         res.set_cookie('username', name, max_age=7 * 24 * 3600)
    #                         res.set_cookie('userpwd', pwd, max_age=7 * 24 * 3600)
    #                     return res
    #         else:
    #             return JsonResponse({'msg': '账号未激活', 'status': 2})
    # except:
    #     return JsonResponse({'msg': '用户名或密码输入不正确', 'status': 0})


def getcaptcha(request):
    image = ImageCaptcha()
    code = random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, 4)
    random_code = "".join(code)
    print(random_code)
    request.session['code'] = random_code
    data = image.generate(random_code)
    return HttpResponse(data, "image/png")

#
def check_name(request):
    name = request.GET.get('name')
    # print(name)
    # 查询 数据库
    if User.objects.filter(name=name):
        return HttpResponse("1")
    else:
        return HttpResponse("0")


def loginout(request):
    return render(request, 'user/logout.html')


def forget_pwd(request):
    return render(request, 'user/forget_pwd.html')


def forget_logic(request):
    name = request.GET.get('user_name')
    email = request.GET.get('email')
    user = User.objects.filter(name=name,email=email)
    print(name,email,user)
    if user:
        ser = Serializer(settings.SECRET_KEY, expires_in=240)  # 声明一个对象
        token = ser.dumps({'id': user[0].id})  # 加密后的令牌 返回值为bytes
        token = token.decode('utf-8')  # 转为字符串
        send_mail('帐户激活', 'http://127.0.0.1:8000/userapp/reset_pwd/?token=' + token, '2970920254@qq.com',
                  ['2970920254@qq.com'], fail_silently=False)
        return JsonResponse({'msg': '发送成功点击修改密码', 'status': 1})
    else:
        return JsonResponse({'msg': '用户或邮箱错误', 'status': 0})
    # else:
    #     return HttpResponse('用户名或邮箱错误')
    # return render(request, 'user/forget_pwd.html')


def reset_pwd(request):
    token = request.GET.get('token')
    request.session['token'] = token
    return render(request, 'user/reset_pwd.html')


def reset_logic(request):
    try:
        pwd = request.POST.get('user-pwd')
        token = request.session.get('token')#  token是未解码的id
        ser = Serializer(settings.SECRET_KEY, expires_in=240)
        id = ser.loads(token).get('id')
        # 在对密码加密
        sha = hashlib.sha256()
        salt = str(uuid.uuid4())
        sha.update((pwd + salt).encode())
        with transaction.atomic():
            user = User.objects.get(pk=id)
            user.password = sha.hexdigest()
            user.salt = salt
            user.save()
            return redirect('userapp:login')
    except:
        return HttpResponse('修改失败')

# #
# def reactive(request):
#     name = request.GET.get("username") # 中获取到要激活的用户的名
#     try:
#         user = User.objects.get(username=name) # 从数据库中查询用户
#         ser = Serializer(settings.SECRET_KEY, expires_in=240)
#         result = ser.dumps({'id': user.id}).decode('utf-8')
#         send_mail('帐户激活', 'http://127.0.0.1:8000/userapp/active/' + result, '2970920254@qq.com',
#                   ['2970920254@qq.com'], fail_silently=False)
#         return JsonResponse({'msg': '邮件发送是成功', 'status': 1})
#     except:
#         return JsonResponse({'msg': '邮件发送是失败', 'status': 0})


