"""
URL configuration for supervision project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("faq/", views.FAQView.as_view(), name="faq"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("generate/", views.GenerateView.as_view(), name="generate"),
    path("", include("allauth.urls")),
    path("change-password/", views.ChangePasswordView.as_view(), name="change"),
    path("teachers/", views.TeachersView.as_view(), name="teachers"),
    path("restrictions/", views.RestrictionsView.as_view(), name="restrictions"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),

]
