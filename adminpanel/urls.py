from django.urls import path
from .views import *

urlpatterns = [
    path('applications/', ApplicationsListView.as_view(), name = "applications_table"),
    path('applications/change-status/<pk>', ChangeStatusView.as_view(), name = "change-status"),
    path('profiles/', ProfilesListView.as_view(), name = "profiles_table"),
    path('profiles/<pk>/detail-information', ProfileDetailView.as_view(), name = "profile-details"),
    path('applicaitons/<pk>', ApplicationDetailView.as_view(), name = "open-app"),
]