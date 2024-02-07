from django.shortcuts import render

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User 

class RegisterView(TemplateView):
        template_name = "register.html"

        def post(self, request):
                data = request.POST.dict() 

                email = data.get("email")
                fname = data.get("fname")
                lname = data.get("lname")
                password = data.get("password")
                cpassword = data.get("cpassword")

                user = User.objects.create_user(fname, email, password)

                return render(request, self.template_name)
                
