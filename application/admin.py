from django.contrib import admin

from application.models import University
from .models import *
from modeltranslation.admin import TranslationAdmin

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country',)

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('country', 'university')

class ApplicationAdmin(TranslationAdmin):
    list_display = ('user', 'type', 'academic_year', 'country', 'university', 'desired_specialty')

# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(TemporaryApplication)
admin.site.register(Application, ApplicationAdmin)