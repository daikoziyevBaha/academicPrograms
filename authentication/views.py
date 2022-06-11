import email
import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from iituidep import settings
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_token
from django.contrib import auth

def send_activation_email(request, user, email_subject, html_path):
    current_site = get_current_site(request)
    email_subject = email_subject # 
    email_body = render_to_string(html_path, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })
    
    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    email.send(fail_silently=False)

# Create your views here.

class FirstNameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        first_name = data['first_name']
        if len(first_name) < 2:
            return JsonResponse({'first_name_error': 'Слишком короткое имя'})
        if not first_name.isalpha():
            return JsonResponse({'first_name_error': 'Имя должно содержать символы из алфавита'})
        return JsonResponse({'first_name_valid': True})

class LastNameValidationView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        last_name = data['last_name']
        if len(last_name) < 2:
            return JsonResponse({'last_name_error': 'Слишком короткая фамилия'})
        if not last_name.isalpha():
            return JsonResponse({'last_name_error': 'Фамилия должна содержать символы из алфавита'})
        return JsonResponse({'last_name_valid': True})

class EmailValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Некорректное имя или домен почты'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Извините, почта с таким именем уже зарегистрирована'})
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        data = request.POST
        context = {
                        "fieldValues" : request.POST
                   }
        if data['first_name'] and data['last_name'] and data['email'] and data['password'] and data['confirm-password']:
            if not User.objects.filter(email = data['email']).exists():
                if len(data['password']) < 8:
                    messages.error(request, "Пароль слишком короткий")
                    return render(request, "authentication/register.html", context)
                if data['password'] != data['confirm-password']:
                    messages.error(request,"Пароли не совпадают")
                    return render(request, "authentication/register.html", context)

                email = data['email']
                password = data['password']
                first_name = data['first_name']
                last_name = data['last_name']
                username = str(email.split('@')[0])
                user = User.objects.create_user(username = username, email = email, first_name = first_name, last_name = last_name)
                user.set_password(password)
                user.is_active = False
                user.save()

                send_activation_email(request, user, "Активируйте свой аккаунт", "authentication/activate.html")
                
                messages.success(request, "Регистрация прошла успешно, подтвердите свой аккаунт на почте")
                return render(request, "authentication/register.html")

        messages.add_message(request, messages.ERROR, "Не все поля заполнены")
        return render(request, "authentication/register.html", context)


def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Ваш аккаунт был подтвержден.')
        return redirect(reverse('login'))

    return render(request, 'authentication/activate-failed.html', {"user": user})



        
class LoginView(View):
    def get(self, request):
        path = 'home' 
        if len(list(request.GET.values())) >= 1:      
            path = list(request.GET.values())[0]
        return render(request, 'authentication/login.html', context = {'path':path})
    def post(self, request):
        redirect_to = request.GET.get('next','')
        print(redirect_to)
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, "Авторизация прошла успешно.")
                    if user.is_superuser:
                        return redirect("/adminpanel/applications/")
                    return redirect(redirect_to)
                messages.add_message(request, messages.ERROR, "Ваш аккаунт не подтвержден, пройдите по ссылке на почте.")
                return render(request, 'authentication/login.html')
            messages.add_message(request, messages.ERROR, "Неправильный логин или пароль.")
            return render(request, 'authentication/login.html')
        messages.add_message(request, messages.ERROR, 'Заполните все поля.')
        return render(request, 'authentication/login.html')
        
        
def logout_user(request):
    auth.logout(request)
    return redirect('incoming')