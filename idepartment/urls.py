from django.urls import path
from .views import *

urlpatterns = [
    path('', incoming, name = 'incoming'),
    path('outgoing', outgoing, name = 'outgoing'),

]