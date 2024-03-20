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
        @staticmethod
        def password_is_valid(password):
                hasUpper = False
                hasLower = False
                hasSpecialCharacter = False
                containsNumber = False
                noSpace = True
                if len(password) >= 8 and len(password) <= 32:
                        for i in range(len(password)):
                                if password[i].isupper():
                                        hasUpper = True
                                elif password[i].islower():
                                        hasLower = True
                                if not password[i].isalnum() and not password[i].isspace():
                                        hasSpecialCharacter = True
                                if password[i].isspace():
                                       noSpace = False
                                if password[i].isdigit():
                                        containsNumber = True
                        if hasUpper == True and hasLower == True and hasSpecialCharacter == True and containsNumber == True and noSpace:
                                return True
                return False
        @staticmethod
        def pword_match(password, cpassword):
                match = True
                if not password == cpassword:
                        match = False
                return match
        @staticmethod
        def email_is_valid(email):
                email_valid = True
                if not "@" in email or not "." in email or " " in email:
                        email_valid = False
                if email_valid:
                       return True
                else:
                       return False
               
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

                if RegisterView.email_is_valid(email) and RegisterView.password_is_valid(password) and RegisterView.pword_match(password, cpassword):
                        try:
                                user = User.objects.create_user(email, email, password)
                                user.first_name = fname
                                user.last_name = lname 
                                user.save()
                                return render(request, self.template_name)
                        except:
                               return render(request, self.template_name, {"state": 4}) # 4 --> email used


                elif not RegisterView.email_is_valid(email):
                       return render(request, self.template_name, {"state": 1}) # 1 --> invalid email
                elif not RegisterView.password_is_valid(password):
                       return render(request, self.template_name, {"state": 2}) # 2 --> invalid password
                else:
                       return render(request, self.template_name, {"state": 3}) # 3 --> passwords do not match

                

                       
        
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