from django.http import HttpResponse
from django.shortcuts import render
from application.models import *
from authentication.models import *
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, View, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib import messages

from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from iituidep import settings
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_token
from django.contrib import auth

# Create your views here.

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


class ApplicationsListView(LoginRequiredMixin, ListView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("applications_table")

    template_name = 'adminpanel/applicationsTable.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.all()

class ApplicationDetailView(LoginRequiredMixin, DetailView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("applications_table")
    model = Application

    template_name =  "adminpanel/one_app.html"
    context_object_name = "application"

    def get_success_url(self):         
        return reverse_lazy('applications_table')

    def post(self, request, pk):
        form = request.POST
        if form['status'] == 'Unreviewed':
            return HttpResponseRedirect(self.get_success_url())
        app = get_object_or_404(Application, pk = pk)
        app.status = form['status']
        app.save()
        messages.add_message(request, messages.SUCCESS, "Статус заявки успешно изменен, студент получил почтовое оповещение.")
        send_activation_email(request, app.user, 'Академическая мобильность', 'adminpanel/status_change.html')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = ['Unreviewed', 'Accepted', 'Declined']
        return context



class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    model = TemporaryApplication
    success_url = reverse_lazy('application')


class ProfilesListView(LoginRequiredMixin, ListView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("profiles_table")

    template_name = 'adminpanel/profilesTable.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all()


class ProfileDetailView(LoginRequiredMixin, DetailView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("profiles_table")

    model = Profile
    template_name = 'adminpanel/profile.html'
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(user = self.request.user)
        return context

class ChangeStatusView(View):
    def post(request):
        print('pk')
        return HttpResponse("okay")