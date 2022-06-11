from modeltranslation.translator import translator, TranslationOptions
from .models import *

class ProfileTranslationOptions(TranslationOptions):
    fields = ('first_name_pi', 'last_name_pi', 'patronymic_pi', 'degree_title_ci', 'contact_person_pi')

translator.register(Profile ,ProfileTranslationOptions)