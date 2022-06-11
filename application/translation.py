from modeltranslation.translator import translator, TranslationOptions
from .models import *

class ApplicationTranslationOptions(TranslationOptions):
    fields = ('desired_specialty',)

translator.register(Application, ApplicationTranslationOptions)