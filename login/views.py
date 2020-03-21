from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import datetime
from django.conf import settings
from django.utils import timezone
# Create your views here.

def index(request):
    if not request.session.get('is_login',None): #不允许重复登录
        return redirect('/login/')
    return render(request,'login/index.html')

def login(request):
    if request.session.get('is_login', None): #不允许重复登录
        return  redirect('/index')
    if request.method == "POST":
        #    username=request.POST.get('username')
        #    password = request.POST.get('password')
        #表单雷获取数据
        login_form = forms.UserForm(request.POST)
        message = '请检查填写内容'
        if login_form.is_valid(): #确保用户名和密码不为空
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                #用户名合法性验证
                user =  models.User.objects.get(name=username)
            except:
                message ='用户不存在'
                return  render(request, 'login/login.html', locals())

            if not user.has_confirmed:
                message = '您尚未进行注册邮件确认，请先前往注册邮箱确认！'
                return  render(request, 'login/login.html', locals())
            if user.password == hash_code(password):  #验证密码正确性
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name']= user.name
                return redirect('/index/')
            else:
                message = '密码不正确'
                return  render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form =forms.UserForm()
    return  render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写内容"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2 :
                message = "两次输入密码不一致！"
                return render(request, 'login/register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name = username)
                if same_name_user:
                    message = "用户名已存在"
                    return  render(request, 'login/register.html',locals())
                same_email_user = models.User.objects.filter(email = email)
                if same_email_user:
                    message = "该邮箱已被注册"
                    return  render(request, 'login/register.html',locals())

                new_user = models.User()
                new_user.name= username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                code = make_confirm_string(new_user)
                send_mail(email,code)
                return redirect('/login/')

        else:
            return render(request, 'login/register.html',locals())
    register_form = forms.RegisterForm()
    return  render(request, 'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush() #清除session
    #或者可以单独清楚指定session
    #del request.session['is_login']
    return  redirect('/login/')

def user_confirm(request):#用户注册确认视图
    code = request.GET.get('code', None)
    message = ''

    try:
        confirm = models.ConfirmString.objects.get(code= code)
    except:
        message = '无效的验证码'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = timezone.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已过期！请重新注册！'
        return  render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "感谢确认，请使用账户登录！"
        return  render(request, 'login/confirm.html', locals())


def hash_code(s,salt='mysite'): #加点盐
    h= hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):  #创建验证码
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)
    return code

def send_mail(email,code): #发送验证邮件
    from  django.core.mail import  EmailMultiAlternatives

    subject = "来自爱圈内的注册确认邮件"

    textContext = '''感谢您注册爱圈内www.iqnei.com，如果您看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员'''
    html_content = '''
    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.iqnei.com</a>爱圈内</p>
    <p>请点击链接完成注册！</p>
    <p>有效期为{}天！</p>
    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject,textContext, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content,"text/html")
    msg.send()