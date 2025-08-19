from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard app routes (landing, dashboard, signup, API, etc.)
    path("", include("dashboard_app.urls")),

    # Authentication (login/logout/password management)
    path("accounts/", include("django.contrib.auth.urls")),
]
