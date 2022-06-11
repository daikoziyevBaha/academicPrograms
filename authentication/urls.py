from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view(), name = 'register'),

    path('validate-email', csrf_exempt(EmailValidationView.as_view()), 
                            name='validate-email'),

    path('validate-first-name', csrf_exempt(FirstNameValidationView.as_view()), 
                            name='validate-first-name'),

    path('validate-last-name', csrf_exempt(LastNameValidationView.as_view()), 
                            name='validate-last-name'),
    path('activate-user/<uidb64>/<token>', activate_user, name='activate'),

    path('login/', LoginView.as_view(), name = 'login'),
    
    path('logout/', logout_user, name = 'logout')
]