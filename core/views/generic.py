from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    """
     A view for the home page.
    """
    template_name = "index.html"


class AboutView(TemplateView):
    """
     A view for the about page.
    """
    template_name = "about.html"


class FAQView(TemplateView):
    """
     A view for the FAQ page.
    """
    template_name = "faq.html"


class SettingsView(TemplateView):
    """
     A view for the settings page.
    """
    template_name = "settings.html"


class GenerateView(TemplateView):
    """
     A view for the generate page.
    """
    template_name = "generate.html"


class RestrictionsView(TemplateView):
    """
     A view for the restrictions page.
    """
    template_name = "restrictions.html"
