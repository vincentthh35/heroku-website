from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from datetime import datetime
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from django.core.mail import EmailMessage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
import os

# Create your views here.

def home(request):
    return render(request, 'home.html', locals())

def redirectToHome(request):
    return HttpResponseRedirect('/index/')

def login(request, user=None):
    if request.method == 'POST':
        form = AuthenticationForm()
        if request.user.is_authenticated:
            return HttpResponseRedirect('/index/')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
        else:
            messages.error(request, 'username or password incorrect')
            return HttpResponseRedirect('.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # valid form
            # try:
            # send email first, and if email successfully sent, create the user
            user = form.save(commit=False)
            user.is_active = False
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = Mail(
                from_email=settings.EMAIL_HOST_USER,
                to_emails=to_email,
                subject=mail_subject,
                html_content=message
            )
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            respose = sg.send(email)
            user.save()
            return render(request, 'registration/message_after_signup.html', {})
            # except:
            #     messages.error(request, 'Sorry, something wrong happened in your registration, please try again later...')
            #     return HttpResponseRedirect('.')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            return HttpResponseRedirect('.')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        # return redirect('home')
        return render(request, 'registration/message_after_activation.html', {})
    else:
        return render(request, 'registration/message_invalid_link.html', {})

def hello_world(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })
    # return HttpResponse("Hello World!")
