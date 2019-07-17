import os
from django.core.mail import send_mail

os.environ['DJANGO_SETTINGS_MODULE']='register.settings'

if __name__=='__main__':
	send_mail(
			'test mail send by www.register.com',
			'welcome to www.register.com, which is a system of register',
			'zldxk777@163.com',
			['919091728@qq.com'],
		 )
