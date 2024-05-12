from django.shortcuts import render

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import RedirectView


class RegisterView(TemplateView):
    """
    A view that allows the user to register.
    """

    template_name = "register.html"

    @staticmethod
    def password_is_valid(password):
        """
        A function that checks if the inputted password is valid
        Args: 
            password (string): the password to be verified
        Returns:
            True or False depending on if the password is valid
        """
        # Creating variables for the conditions that need to be met for a password to be valid.
        has_upper = False
        has_lower = False
        has_special_character = False
        contains_number = False
        has_space = False
        # Making sure that the password is at least 8 characters
        if len(password) >= 8:
            # Checking each character to make sure the conditions are met
            for i in range(len(password)):
                if password[i].isupper():
                    has_upper = True
                elif password[i].islower():
                    has_lower = True
                if not password[i].isalnum() and not password[i].isspace():
                    has_special_character = True
                if password[i].isspace():
                    has_space = True
                if password[i].isdigit():
                    contains_number = True
        # Returning a boolean based on if the password meets the conditions or not.
        return (
            has_upper
            and has_lower
            and has_special_character
            and contains_number
            and not has_space
        )

    @staticmethod
    def pword_match(password, cpassword):
        """
        Checks if the password and confirm password are the same
        Args: 
            password (string): the password to be verified
            cpassword (string): the password to be verified with
        Returns:
            True or False depending on if the password and cpassword are the same
        """
        return password == cpassword

    @staticmethod
    def email_is_valid(email):
        """
        Checks if there is an @ and . in the email. Also makes sure there's no spaces.
        Args: 
            email (string): the email to be verified
        Returns:
            True or False depending on if the email is valid or not.
        """
        return "@" in email and "." in email and not " " in email

    def post(self, request):
        """
        Gets information about the user's email, name, and password and saves it into the database if valid
        Args: 
            request (data): the request of the post function containing the form data.
        Returns:
            (Http response)
        """
        # Storing the information inputted by the user in variables
        data = request.POST.dict()
        email = data.get("email")
        fname = data.get("fname")
        lname = data.get("lname")
        password = data.get("password")
        cpassword = data.get("cpassword")

        # Checking that the email and password are valid and that the passwords match.
        if (
            RegisterView.email_is_valid(email)
            and RegisterView.password_is_valid(password)
            and RegisterView.pword_match(password, cpassword)
        ):
            # Here, we attempt to add the user to the database. If this email is in use, it will throw an error and the program goes to the except case.
            try:
                # Uploading the user's information
                user = User.objects.create_user(email, email, password)
                user.first_name = fname
                user.last_name = lname
                user.save()
                return render(request, self.template_name)
            except:
                # Setting the state to 4 so that an error toast appears on the website (see register.html)
                return render(
                    request, self.template_name, {"state": 4}
                )  # 4 --> email used

        # Here, we use "state" to determine which error toast should be shown.
        elif not RegisterView.email_is_valid(email):
            return render(
                request, self.template_name, {"state": 1}
            )  # 1 --> invalid email
        elif not RegisterView.password_is_valid(password):
            return render(
                request, self.template_name, {"state": 2}
            )  # 2 --> invalid password
        else:
            return render(
                request, self.template_name, {"state": 3}
            )  # 3 --> passwords do not match


class LoginView(TemplateView):
    """
    A view that allows the user to login.
    """

    template_name = "login.html"

    def post(self, request):
        """
        Gets user information and authenticates it
        Args: 
            request (data): the request of the post function containing the form data.
        Returns:
            (Http response)
        """
        # Putting the email and password into variables
        data = request.POST.dict()
        email = data.get("email")
        password = data.get("password")
        # Using authenticate to make sure that the password is correct and that the email is registered.
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user) #login if valid
        
        return render(request, self.template_name)


class LogoutView(RedirectView):
    """
    A view to logout user and redirect to homepage.
    """

    permanent = False
    query_string = True
    pattern_name = "index"

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated:
            logout(self.request) #logout user
        return super(LogoutView, self).get_redirect_url(*args, **kwargs) #return to home page.


class ChangePasswordView(RedirectView):
    """
     A view for saving changing user password
    """

    template_name = "change_password.html"

    def post(self, request):
        """
        Gets user information and authenticates it
            Args: 
                request (data): the request of the post function containing the form data.
            Returns:
                (Http response)
        """
        data = request.POST.dict()
        old_password = data.get("password")
        new_password = data.get("newpassword")
        new_password_c = data.get("confpassword")

        request.user.password = new_password
        request.user.save() # save new password

        return render(request, self.template_name)
