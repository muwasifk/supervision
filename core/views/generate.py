from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
import hashlib 

from core.models import Schedule

class GenerateView(TemplateView): 
    template_name = "generate.html"

    def post(self, request):
        data = request.POST.dict()
        print(data.get("name"))
        schedule = Schedule(
            schedule_id = hashlib.md5((str(data.get("name")) + str(data.get("school-name"))).encode('utf-8')).hexdigest(),
            name = data.get("name"),
            first_name = request.user.first_name,
            last_name = request.user.last_name,
            email = request.user.email, 
            school = data.get("school-name"),
            city = data.get("city"),
            country = data.get("country")
        )

        schedule.save() 

        return redirect('/teachers/')

class TeachersView(TemplateView):
    template_name = "teachers.html"