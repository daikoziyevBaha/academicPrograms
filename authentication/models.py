from django.db import models
from django.contrib.auth.models import User
from application.models import Country, University
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Мужской'),
        ('FEMALE', 'Женский')
    ]
    DEGREES = [
        ('BA', 'Bachelors degree'),
        ('MA', 'Masters degree')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name_pi = models.CharField(verbose_name = _("Имя"), max_length=255, blank=True, null=True)
    last_name_pi = models.CharField(verbose_name = _("Фамилия"), max_length=255, blank=True, null=True)
    patronymic_pi = models.CharField(verbose_name = _("Отчество"), max_length=255, blank=True, null=True)
    email_pi = models.EmailField(verbose_name = _("Почта"), unique=True, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате +9999999999 от 9 до 15 символо.")
    phone_pi = models.CharField(verbose_name = _("Номер телефона"), validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    birth_date_pi = models.DateField(verbose_name = _("Дата рождения"), auto_now_add=False, blank=True, null = True)
    gender_pi = models.CharField(verbose_name = _("Пол"), choices=GENDER_CHOICES, blank=True, null=True, max_length=255)
    country_ci = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    university_ci = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    start_year_ci = models.CharField(verbose_name = _("Начало обучения"), max_length=4, blank=True, null=True)
    graduation_year_ci = models.CharField(verbose_name = _("Выпуск"), max_length=4, blank=True, null=True)
    degree_title_ci = models.CharField(verbose_name = _("Степень"), choices=DEGREES, blank=True, null=True, max_length=255)
    specialty_ci = models.CharField(verbose_name = _("Специальность"), max_length=255, blank=True, null=True)
    passport_id_pi = models.CharField(verbose_name = _("Номер паспорта"), max_length=20, blank=True, null=True, validators = [RegexValidator(
            regex=r'^[a-zA-Z\d0-20]*$',
            message='Паспорт ID должен состоять из цифр или букв алфавита')])
    passport_authority_pi = models.CharField(verbose_name = _("Кем выдан"), max_length=30, blank=True, null=True)
    date_of_issue_pi = models.DateField(verbose_name = _("Дата выдачи"), auto_now_add=False, blank=True, null=True)
    date_of_expiry_pi = models.DateField(verbose_name = _("Дата просрочки"), auto_now_add=False, blank=True, null=True)
    contact_person_pi = models.CharField(verbose_name = _("Контактное лицо"), max_length=255, blank=True, null=True)
    contact_person_phone_pi = models.CharField(verbose_name = _("Номер контактного лица"), max_length=12, blank=True, null=True, validators=[phone_regex])
    contact_person_email_pi = models.EmailField(verbose_name = _("Почта контактного лица"), blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Profile.objects.create(user=instance, first_name_pi = instance.first_name, last_name_pi = instance.last_name, email_pi = instance.email)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()

    