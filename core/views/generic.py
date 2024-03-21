from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class FAQView(TemplateView):
    template_name = "faq.html"

class SettingsView(TemplateView): 
    template_name = "settings.html"

class GenerateView(TemplateView): 
    template_name = "generate.html"

class RestrictionsView(TemplateView): 
    template_name = "restrictions.html"

class CalendarView(TemplateView): 
    template_name = "calendar.html"