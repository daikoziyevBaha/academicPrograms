from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import os
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Country(models.Model):
    country = models.CharField(verbose_name = _("Страна"), max_length=255, blank = True, null = False)
    
    def __str__(self) -> str:
        return self.country


class University(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    university = models.CharField(verbose_name=_("Университет"), max_length=255, blank=True, null = False)
    
    def __str__(self) -> str:
        return self.university

class TemporaryApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(verbose_name=_("Данные"), default = dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id) + ' ' + self.user.get_full_name()


def my_awesome_upload_function(instance, filename):
    """ this function has to return the location to upload the file """
    return os.path.join(instance.get_user_name().lower(), filename)

class Application(models.Model):
    STATUS = (  
    ('Unreviewed', 'Unreviewed'),
    ('Accepted', 'Accepted'),
    ('Declined', 'Declined'),
    )
    ACADEMIC_YEAR = (
        ('2021 - 2022', '2021 - 2022'),
        ('2022 - 2023', '2022 - 2023'),
    )
    TYPE = (
        ('INCOMING', 'INCOMING'),
        ('OUTGOING', 'OUTGOING')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("Тип мобильности"), choices=TYPE, max_length=20, blank=True, null=True)
    academic_year = models.CharField(verbose_name = _("Академический год"),choices=ACADEMIC_YEAR, max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    desired_specialty = models.CharField(verbose_name = _("Желаемая специальность"), max_length=255, blank=True, null=True)
    passport = models.FileField(verbose_name = _("Скан паспорта"), upload_to=my_awesome_upload_function, blank=True, null=True)
    transcript = models.FileField(verbose_name = _("Скан транскрипта"), upload_to=my_awesome_upload_function, blank=True, null=True)
    motivation = models.FileField(verbose_name = _("Скан мотивационного письма"),upload_to=my_awesome_upload_function, blank=True, null=True)
    english = models.FileField(verbose_name = _("Скан английского"),upload_to=my_awesome_upload_function, blank=True, null=True)
    recommendation = models.FileField(verbose_name = _("Скан рекоммендации"),upload_to=my_awesome_upload_function, blank=True, null=True)
    status = models.CharField(verbose_name = _("Статус заявки"), choices=STATUS, max_length=100, default=STATUS[0][0])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)

    def get_user_name(self):
        return str(self.user.last_name + '_' + self.user.first_name)
