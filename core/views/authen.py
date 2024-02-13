from django.shortcuts import render

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login 

class RegisterView(TemplateView):
        template_name = "register.html"        

        def post(self, request):
                data = request.POST.dict() 

                email = data.get("email")
                fname = data.get("fname")
                lname = data.get("lname")
                password = data.get("password")
                cpassword = data.get("cpassword")

                user = User.objects.create_user(email, email, password)

                return render(request, self.template_name)
        
class LoginView(TemplateView): 

        template_name = "login.html"
        def post(self, request):
                data = request.POST.dict()
                email = data.get("email")
                password = data.get("password")
                user = authenticate(username = email, password = password)
                if user is not None: 
                        login(request, user)

                return render(request, self.template_name)
