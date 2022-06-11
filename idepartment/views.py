from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, View, FormView
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
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
# Create your views here.
menu = [{'title': "Департамент международного сотрудничества", 'url_name': 'home'},
        {'title': "Академическая мобильность", 'url_name': 'exchange'},
        {'title' : 'Входящий студент', 'url_name': 'incoming'},
        {'title' : 'Исходящий студент', 'url_name': 'outgoing'}
]

def exchange_info(request):
    context = {
        'menu' : menu
    }
    return render(request, 'idepartment/exchange.html', context)

def incoming(request):
    context = {
        'menu' : menu
    }
    return render(request, 'idepartment/incoming.html', context)

def outgoing(request):
    context = {
        'menu' : menu
    }
    return render(request, 'idepartment/outgoing.html', context)