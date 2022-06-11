from dataclasses import fields
import datetime
import email
from random import choices
from tkinter.tix import Select
from wsgiref.validate import validator
from xml.etree.ElementInclude import include
from django import forms
from authentication.models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from phone_field import PhoneField
from .models import *
from django.contrib.auth.models import User
from validate_email import validate_email
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CountryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%obj.country

class UniversityModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s"%obj.university

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user','country_ci','university_ci','degree_title_ci', 'specialty_ci', 'start_year_ci', 'graduation_year_ci']

        widgets = {
            "first_name_pi": forms.TextInput(attrs={"class":"form-control"}),
            "last_name_pi": forms.TextInput(attrs={"class":"form-control"}),
            "patronymic_pi": forms.TextInput(attrs={"class":"form-control"}),
            "phone_pi": forms.TextInput(attrs={"class":"form-control"}),
            "birth_date_pi": forms.DateInput(attrs={"class":"form-control", "data-date-format": "yyyy-mm-dd"}),
            "gender_pi": forms.Select(attrs={"class":"form-control"}),
            "passport_id_pi": forms.TextInput(attrs={"class":"form-control"}),
            "email_pi": forms.EmailInput(attrs={"class":"form-control"}),
            "passport_authority_pi": forms.TextInput(attrs={"class":"form-control"}),
            "date_of_issue_pi": forms.DateInput(attrs={"class":"form-control", "data-date-format": "yyyy-mm-dd"}),
            "date_of_expiry_pi": forms.DateInput(attrs={"class":"form-control", "data-date-format": "yyyy-mm-dd"}),
            "contact_person_pi": forms.TextInput(attrs={"class":"form-control"}),
            "contact_person_phone_pi": forms.TextInput(attrs={"class":"form-control"}),
            "contact_person_email_pi": forms.EmailInput(attrs={"class":"form-control"})
        }
    

class CurriculumForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['country_ci','university_ci','degree_title_ci', 'specialty_ci', 'start_year_ci', 'graduation_year_ci']
        widgets = {
            'country_ci': forms.Select(attrs={'class':'form-select', 'aria-label':'Default select example'}),
            'university_ci': forms.Select(attrs={'class':'form-select', 'aria-label':'Default select example'}),
            'degree_title_ci': forms.Select(attrs={'class':'form-select', 'aria-label':'Default select example'}),
            'specialty_ci': forms.TextInput(attrs={'class':'form-control', 'aria-label':'Default select example'}),
            'start_year_ci': forms.TextInput(attrs={'class':'form-control', 'aria-label':'Default select example'}),
            'graduation_year_ci': forms.TextInput(attrs={'class':'form-control', 'aria-label':'Default select example'})
        }

class CreateApplicationForm(forms.Form):
    ACADEMIC_YEAR = (
        ('2021 - 2022', '2021 - 2022'),
        ('2022 - 2023', '2022 - 2023'),
    )
    TYPE = (
        ('INCOMING', 'INCOMING'),
        ('OUTGOING', 'OUTGOING')
    )
    countries = Country.objects.order_by('-country')
    universities = University.objects.order_by('-university')
    type = forms.ChoiceField(required = True, choices=TYPE, 
                                widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}))
    academic_year = forms.ChoiceField(required = True, choices = ACADEMIC_YEAR, 
                                widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}))
    country = forms.ChoiceField(required = True,choices = tuple((country.country,country.country,) for country in countries), 
                                widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}) )
    university = forms.ChoiceField(required = True,choices = tuple((university.university,university.university,) for university in universities), 
                                widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}))
    desired_specialty = forms.CharField(required = True, widget=forms.TextInput(attrs={'class':'form-control'}), min_length=3)


class ExchangeInfoEditForm(forms.Form):
    ACADEMIC_YEAR = (
        ('2021 - 2022', '2021 - 2022'),
        ('2022 - 2023', '2022 - 2023'),
    )
    TYPE = (
        ('INCOMING', 'INCOMING'),
        ('OUTGOING', 'OUTGOING')
    )
    countries = Country.objects.order_by('-country')
    universities = University.objects.order_by('-university')
    type = forms.ChoiceField(choices=TYPE, widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}))
    academic_year = forms.ChoiceField(choices = ACADEMIC_YEAR, widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}))
    country = forms.ChoiceField(choices = tuple((country.country,country.country,) for country in countries), 
                                widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}) )
    university = forms.ChoiceField(choices = tuple((university.university,university.university,) for university in universities), 
                                widget = forms.Select(attrs={'class':'form-select', 'aria-label': 'Default select example'}))
    desired_specialty = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), min_length=3)

class DocumentsEditForm(forms.Form):
    application_id = forms.CharField(widget=forms.HiddenInput())
    passport_scan = forms.FileField(required=False, 
                                    widget=forms.FileInput(attrs={'class': 'form-control', 'accept':'image/jpeg,image/png,application/pdf'}))
    transcript_scan = forms.FileField(required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'accept':'image/jpeg,image/png,application/pdf'}))
    english_scan = forms.FileField(required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'accept':'image/jpeg,image/png,application/pdf'}))
    motivation_scan = forms.FileField(required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'accept':'image/jpeg,image/png,application/pdf'}))
    recommendation_scan = forms.FileField(required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'accept':'image/jpeg,image/png,application/pdf'}))
    vaccination_scan = forms.FileField(required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control', 'accept':'image/jpeg,image/png,application/pdf'}))


