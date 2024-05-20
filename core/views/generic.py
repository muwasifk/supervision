"""
generic.py 
ICS4U SDP 
Muhammad Wasif Kamran, Karan Chawla, Eric Sui
Handles the rendering and routing of basic ``flatpages" 
"""

# Django imports 
from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

"""
Codebase uses Class-Based Views (CBV) for Django views 
Each page can be defined by a class and the ``template_name" is what Django will
render on the frontend 
https://docs.djangoproject.com/en/5.0/topics/class-based-views/
"""

class IndexView(TemplateView):
    """
    Home page view using index.html 
    """
    template_name = "index.html"


class AboutView(TemplateView):
    """
    About page view using about.html 
    """
    template_name = "about.html"


class FAQView(TemplateView):
    """
    FAQ page view using faq.html
    """
    template_name = "faq.html"


class SettingsView(TemplateView):
    """
     A view for the settings page.
    """
    template_name = "settings.html"


class GenerateView(TemplateView):
    """
    Generate page view using generate.html
    """
    template_name = "generate.html"