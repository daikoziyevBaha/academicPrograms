from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, View, FormView, DeleteView
from .forms import *
from django.urls import reverse, reverse_lazy
from .models import *
from django.contrib import messages
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from iituidep import settings
from authentication.views import *
from django.forms.models import model_to_dict
from authentication.models import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
menu = [{'title': "Департамент международного сотрудничества", 'url_name': 'home'},
        {'title': "Академическая мобильность", 'url_name': 'exchange'},
        {'title' : 'Входящий студент', 'url_name': 'incoming'},
        {'title' : 'Исходящий студент', 'url_name': 'outgoing'}
]

# {'title': "Партнерские отношения", 'url_name': 'partners'}
def profile_fill_status(data, ends, accept):
    data = model_to_dict(data)
    fields = accept
    count = 0
    for key, value in data.items():
        if key.endswith(ends) and value is not None and key != "patronymic_pi":
            count += 1
    if count >= fields:
        return True
    else:
        return False

def documents_fill_status(data):
    fields = 6
    count = 0
    for key in data:
        if key.endswith('scan') and key is not None:
            count += 1
    if count >= fields:
        return True
    else:
        return False

def exchangeinfo_fill_status(data):
    fields = 4
    count = 0
    for key in data:
        if not key.endswith('scan') and key is not None:
            count += 1
    if count >= fields:
        return True
    else:
        return False

def merge_dicts(*dict_args):
    """
    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence goes to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

class ApplicationView(LoginRequiredMixin, View):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    def get(self, request):
        applications = list()
        app_objects = TemporaryApplication.objects.filter(user = request.user)
        for app in app_objects:
            data = json.loads(app.data)
            data['id'] = app.id
            applications.append(data)
        profile = request.user.profile
        personal_status = profile_fill_status(profile, 'pi', 13)
        curriculum_status = profile_fill_status(profile, 'ci', 6)
        context = {
            'menu' : menu,
            'applications' : applications,
            'personal_status' : personal_status,
            'curriculum_status' : curriculum_status
        }
        return render(request, 'application/application.html', context)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    model = Profile
    form_class = ProfileForm
    template_name = 'application/profile.html'
    object = None
    module = None

    def has_permission(self, request):
        return request.user.is_active

    def get_success_url(self):
        return reverse('application')
        
    def get_module(self):
        object = self.object if getattr(self, 'object', None) is not None else self.get_object()
        return object.load_module()

    def get_settings_form_kwargs(self):
        kwargs = {
            'initial': self.module.settings
        }

class CurriculumEditView(LoginRequiredMixin, UpdateView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    model = Profile
    form_class = CurriculumForm
    template_name = 'application/curriculum.html'
    object = None
    module = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def has_permission(self, request):
        return request.user.is_active

    def get_success_url(self):
        return reverse('application')
        
    def get_module(self):
        object = self.object if getattr(self, 'object', None) is not None else self.get_object()
        return object.load_module()

    def get_settings_form_kwargs(self):
        kwargs = {
            'initial': self.module.settings
        }

class NewApplicationView(LoginRequiredMixin, FormView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    template_name = "application/createapplication.html"
    form_class = CreateApplicationForm
    success_url = "/application"

    def form_valid(self, form):
        data = json.dumps(form.cleaned_data)
        application = TemporaryApplication.objects.create(user = self.request.user, data = data)
        return super().form_valid(form)

class CloseCreateView(View):
    def get(self, request):
        return redirect("application")

class ApplicationDetails(LoginRequiredMixin, View):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    def get(self, request, pk):
        application = TemporaryApplication.objects.get(pk = pk)
        data = json.loads(application.data)
        status = dict()
        status['personal'] = profile_fill_status(request.user.profile, 'pi', 13)
        status['curriculum'] = profile_fill_status(request.user.profile, 'ci', 6)
        status['documents'] = documents_fill_status(data)
        status['exchangeinfo'] = exchangeinfo_fill_status(data)
        context = {
            'application' : application,
            'status' : status
        }
        return render(request, 'application/application_details.html', context)

    def post(self, request, pk):
        t_application = TemporaryApplication.objects.get(pk = pk)
        data = json.loads(t_application.data)
        for files in data:
            if files.endswith('scan'):
                data[files] = data[files].split('/media')[1]
        if documents_fill_status(data) and exchangeinfo_fill_status(data) and profile_fill_status(request.user.profile, 'pi', 13) and profile_fill_status(request.user.profile, 'ci', 6):
            country = Country.objects.get(country = data['country'])
            university = University.objects.get(university = data['university'])
            application = Application.objects.create(id = t_application.id, type = data['type'], user = request.user, academic_year = data['academic_year'],
                                                    country_id = country.id, university_id = university.id, desired_specialty = data['desired_specialty'],
                                                    passport = data['passport_scan'], transcript = data['transcript_scan'], motivation = data['motivation_scan'], 
                                                    english = data['english_scan'], recommendation = data['recommendation_scan'])
            t_application.delete()
            send_activation_email(request, request.user, 'Ваша заявка успешно принита', 'application/application_success.html')
        return redirect("application")

class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    model = TemporaryApplication
    success_url = reverse_lazy('application')


class ExchangeInfoUpdateView(LoginRequiredMixin, FormView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    template_name = 'application/exchange_info.html'
    form_class = ExchangeInfoEditForm
    success_url = reverse_lazy('application-details')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        return context 

    def get_initial(self, **kwargs):
        application = TemporaryApplication.objects.get(pk = self.kwargs['pk'])
        initial = super().get_initial()
        initial = json.loads(application.data)
        return initial
    
    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('application-details', kwargs = {'pk': kwargs['pk']})
        else:
            return reverse_lazy('application')

    def form_valid(self, form):
        application = TemporaryApplication.objects.get(pk = self.kwargs['pk'])
        application.data = json.dumps(merge_dicts(json.loads(application.data), form.cleaned_data))
        application.save()
        return HttpResponseRedirect(self.get_success_url(pk = self.kwargs['pk']))
    
    
class DocumentsEditView(LoginRequiredMixin, FormView):
    login_url = "/authentication/login"
    redirect_field_name = reverse_lazy("application")

    template_name = 'application/documents_edit.html'
    form_class = DocumentsEditForm
    success_url = reverse_lazy('application-details')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def get_initial(self, **kwargs):
        application = TemporaryApplication.objects.get(pk = self.kwargs['pk'])
        initial = super().get_initial()
        documents_data = json.loads(application.data)
        initial = documents_data
        initial['application_id'] = str(application.id)
        return initial

    def get_success_url(self, **kwargs):         
        if  kwargs != None:
            return reverse_lazy('application-details', kwargs = {'pk': kwargs['pk']})
        else:
            return reverse_lazy('application')

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url(pk = self.kwargs['pk']))


def add_document_ajax(request):
    print("yes")
    if request.method == 'POST' and request.is_ajax():
        dir_storage = os.path.join(settings.MEDIA_ROOT, str(request.user.last_name + '_' + request.user.first_name).lower())
        url_storage = os.path.join(settings.MEDIA_URL, str(request.user.last_name + '_' + request.user.first_name).lower())
        application = TemporaryApplication.objects.get(pk = request.POST['application_id'])
        data = json.loads(application.data)
        documents = request.FILES
        file_names_list = ['passport_scan', 'transcript_scan', 'english_scan', 'motivation_scan', 'recommendation_scan', 'vaccination_scan']
        for file in file_names_list:
            if file in documents:
                file_storage = FileSystemStorage(location=dir_storage, base_url=dir_storage)
                filename = file_storage.save(request.FILES[file].name, request.FILES[file])
                print(filename, type(filename), file_storage)
                data[file] = url_storage + '/' + filename
                application.data = json.dumps(data)
                application.save()
            
        return JsonResponse({'error':'Success'})



