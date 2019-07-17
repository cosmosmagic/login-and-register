from django.shortcuts import render,redirect
from .models import User,ConfirmString
from . import forms
import hashlib
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


# Create your views here.

def index(request):
	if not request.session.get('is_login',None):
		return redirect('/login/')
	return render(request,'login/index.html')


def login(request):
	if request.session.get('is_login',None):
		return redirect('/index/')
	if request.method=="POST":
		login_form=forms.UserForm(request.POST)
		message="please check your content!"
		if login_form.is_valid():
			username=login_form.cleaned_data.get('username')
			password=login_form.cleaned_data.get('password')

			try:
				user=User.objects.get(name=username)
			except:
				message="user doesn's exist!"
				return render(request,'login/login.html',locals())

			if not user.has_confirmed:
				message='the account has not confirm with email'
				return render(request,'login/login.html',locals())

			if user.password==hash_code(password):
				request.session['is_login']=True
				request.session['user_id']=user.id
				request.session['user_name']=user.name
				return redirect('/index/')
			else:
				message="password is incorrect"
				return render(request,'login/login.html',locals())
		else:
			return render(request,'login/login.html',locals())
	login_form=forms.UserForm()
	return render(request,'login/login.html',locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "please check your content!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = 'the two passwords is inconsistent!'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = 'the username is exist!'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = 'the email is exist!'
                    return render(request, 'login/register.html', locals())

                new_user = User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex

                new_user.save()
                code=make_confirm_string(new_user)
                send_email(email,code)
                message='please identify to your email'
                return render(request,'login/confirm.html',locals())
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
	if not request.session.get('is_login',None):
		return redirect('/login/')
	request.session.flush()
	# del request.session['is_login']
	# del request.session['user_id']
	# del request.session['user_name']
	return redirect('/login/')

def hash_code(s,salt='register'):
	h=hashlib.sha256()
	s+=salt
	h.update(s.encode())
	return h.hexdigest()

def make_confirm_string(user):
	now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	code=hash_code(user.name,now)
	ConfirmString.objects.create(code=code,user=user,)
	return code

def send_email(email,code):
	subject='register confirm mail send by wwww.register.com'
	text_content='''thank for your registering wwww.register.com,\
			if you see this message,your mail server don't\
			refer link of HTML, please contact administrator'''
	html_content='''
			<p>thank for your registering<a href="http://{}/confirm/?code={}"\
			target=blank>www.register.com</a></p>
			<p>please click link to complete register</p>
			<p>period of validity of link is {} days</p>
		     '''.format('127.0.0.1:8000',code,settings.CONFIRM_DAYS)

	msg=EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
	msg.attach_alternative(html_content,"text/html")
	msg.send()

def user_confirm(request):
	code=request.GET.get('code',None)
	message=''
	try:
		confirm=ConfirmString.objects.get(code=code)
	except:
		message='invalid request'
		return render(request,'login/confirm.html',locals())

	c_time=confirm.c_time
	now=datetime.datetime.now()
	if now>c_time+datetime.timedelta(settings.CONFIRM_DAYS):
		confim.user.delete()
		message='your email is exceed the time limit, please register restart'
		return render(request,'login/confim.html',locals())
	else:
		confirm.user.has_confirmed=True
		confirm.delete()
		message='thank for your indentify, please register by account'
		return render(request,'login/confirm.html',locals())

