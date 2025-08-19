from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/api/indicator-data/", views.get_indicator_data, name="indicator_data"),
]
