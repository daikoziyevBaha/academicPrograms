from django.contrib import admin

from authentication.models import Profile
from modeltranslation.admin import TranslationAdmin
# Register your models here.

class ProfieAdmin(TranslationAdmin):
    list_display = ['user', 'email_pi', 'phone_pi', 'birth_date_pi','country_ci', 'university_ci']

admin.site.register(Profile, ProfieAdmin)