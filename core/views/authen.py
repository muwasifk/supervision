from django.shortcuts import render

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.views.generic import RedirectView

class RegisterView(TemplateView):
        """
        A view that allows the user to register
        """
        template_name = "register.html"        

        def post(self, request):
                """
                Gets information about the user's email, name, and password and saves it into the database
                """
                data = request.POST.dict() 

                email = data.get("email")
                fname = data.get("fname")
                lname = data.get("lname")
                password = data.get("password")
                cpassword = data.get("cpassword")

                user = User.objects.create_user(email, email, password)
                user.first_name = fname
                user.last_name = lname 
                user.save() 

                return render(request, self.template_name)
        
class LoginView(TemplateView): 
        """
        A view that allows the user to login
        """
        template_name = "login.html"

        def post(self, request):
                """
                Gets user information and authenticates it
                """
                data = request.POST.dict()
                email = data.get("email")
                password = data.get("password")
                user = authenticate(username = email, password = password)
                if user is not None: 
                        login(request, user)

                return render(request, self.template_name)

class LogoutView(RedirectView):
    """
    A view that logout user and redirect to homepage.
    """
    permanent = False
    query_string = True
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)