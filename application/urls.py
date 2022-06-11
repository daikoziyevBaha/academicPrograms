from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', ApplicationView.as_view(), name = 'application'),
    path('profile-edit/<pk>', ProfileEditView.as_view(), name = 'profile-edit'),
    path('curriculum-edit/<pk>', CurriculumEditView.as_view(), name = 'curriculum-edit'),
    path('create-application/', NewApplicationView.as_view(), name = 'create-application'),
    path('<pk>/delete/', ApplicationDeleteView.as_view(), name = 'delete-application'),
    path('application-details/<pk>', ApplicationDetails.as_view(), name = 'application-details'),
    path('application-details/<pk>/exchangeinfo-edit', ExchangeInfoUpdateView.as_view(), name = 'exchangeinfo-edit'),
    path('application-details/<pk>/documents-edit', DocumentsEditView.as_view(), name = 'documents-edit'),
    path('application-details/documents-edit/add-document', csrf_exempt(add_document_ajax), name = 'add-document'),
    path('create-application/close-createapp/', CloseCreateView.as_view(), name = 'close-createapp')
]