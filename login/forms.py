from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
	username=forms.CharField(label="username",max_length=128,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username','autofocus':''}))
	password=forms.CharField(label="password",max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	captcha=CaptchaField(label='Verification')

class RegisterForm(forms.Form):
	gender=(
			('male','Sir'),
			('female','Lady'),
	       )
	username=forms.CharField(label='username',max_length=128,widget=forms.TextInput(attrs={'class':'form-control','autofocus':''}))
	password1=forms.CharField(label='password',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2=forms.CharField(label='confirm',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control',}))
	email=forms.EmailField(label='email address',widget=forms.EmailInput(attrs={'class':'form-control'}))
	sex=forms.ChoiceField(label='gender',choices=gender)
	captcha=CaptchaField(label='Verification')
