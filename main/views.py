from base64 import urlsafe_b64encode
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
import email
from email import message
from django.shortcuts import render, redirect
from multiprocessing import context
from .form import RegisterForm, LoginForm
from django.contrib.auth import login as login_process, logout as logout_process, authenticate
from django.contrib import messages
from Account import views
from django.contrib.auth.decorators import login_required
from main import form

# here we use the tag login_process because of def login there is after (conflit between them)

# Create your views here.

@login_required(login_url='/login')
def home(request):
    return render(request, 'shared/home.html')

    
def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login_process(request, user)
                return redirect(views.createAccount)
                
        else :
            form = RegisterForm()    
        	
        return render(request, 'registration/sign_up.html', {"form": form})
    else :
       return redirect('/home')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_b64encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})