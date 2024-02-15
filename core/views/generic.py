from django.shortcuts import render

from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class FAQView(TemplateView):
    template_name = "faq.html"

class SettingsView(TemplateView): 
    template_name = "settings.html"

    