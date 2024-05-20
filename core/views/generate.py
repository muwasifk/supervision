"""
generate.py
ICS4U SDP
Muhammad Wasif Kamran, Karan Chawla, Eric Sui 
All relevant views for preprocessing data before generating a calendar 
"""
# Django imports
from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
from core.models import Schedule, ScheduleList, Teacher

# Other Python imports (for hashing and for CSV handling)
import hashlib
import csv

class GenerateView(TemplateView):
    """
    CBV for generate page 
    """
    # Use generate.html file 
    template_name = "generate.html"

    def post(self, request):
        """
        Gets user information and authenticates it
            Args: 
                request (data): the request of the post function containing the form data.
            Returns:
                (Http response)
        """
        data = request.POST.dict()

        # Parse data from form
        schedule = Schedule(
            schedule_id=hashlib.md5(
                (str(data.get("name")) + str(data.get("school-name"))).encode("utf-8")
            ).hexdigest(),
            name=data.get("name"),
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            school=data.get("school-name"),
            city=data.get("city"),
            country=data.get("country"),
        )

        # Save it to database 
        schedule.save() 

        # A check to save the id of the schedules created
        check = ScheduleList.objects.filter(email=request.user.email).values()
        if len(check) == 0:
            # If no previous schedules found, create a new row
            id = ScheduleList(
                email=request.user.email,
                schedules=[
                    hashlib.md5(
                        (str(data.get("name")) + str(data.get("school-name"))).encode(
                            "utf-8"
                        )
                    ).hexdigest()
                ],
            )

            id.save()
        else:
            # If previous schedules found for this account, append to existing row
            row = ScheduleList.objects.get(email=request.user.email)
            row.schedules.append(
                hashlib.md5(
                    (str(data.get("name")) + str(data.get("school-name"))).encode(
                        "utf-8"
                    )
                ).hexdigest()
            )

            row.save()

        # after id retrieved, move on to next step (teachers)
        return redirect("/teachers/")


class TeachersView(TemplateView):
    """
    CBV for teacher data page 
    """
    # Use teachers.html 
    template_name = "teachers.html"

    def get(self, request):
        """
        Handles GET requests from the browser 
            Args: 
                request (data): the request of the HTML header 
            Returns:
                (Http response)
        """
        # Find the row of the schedule and then the rows of the teachers to be displayed in a HTML table 
        row = ScheduleList.objects.get(email=request.user.email)
        rows = Teacher.objects.all().filter(schedule_id=row.schedules[-1])

        return render(request, self.template_name, {"rows": rows})

    def post(self, request):
        """
        Gets teacher information and saves it
            Args: 
                request (data): the data from the POST request
            Returns:
                (Http response) - rows of teachers in schedule
        """
        if "contract" in request.POST: # Differentiates between submit POST and form POST 
                # Parse data then save to database
                data = request.POST.dict()
                row = ScheduleList.objects.get(email=request.user.email)
                teacher = Teacher(
                schedule_id=row.schedules[-1],
                first_name=data.get("fname"),
                last_name=data.get("lname"),
                email=data.get("email"),
                contract=data.get("contract"),
                schedule=data.get("schedule"),
                )
                teacher.save()
        else: # This means that user submitted a CSV file 
                # Read data from CSV file
                row = ScheduleList.objects.get(email=request.user.email)
                ifile = request.FILES["teachersx"]
                decoded_file = ifile.read().decode('utf-8').splitlines()
                data  = csv.DictReader(decoded_file)

                # Using CSV data, create Teacher objects and save to the database
                for rows in data:
                        teacher = Teacher(
                        schedule_id=row.schedules[-1],
                        first_name=rows["fname"],
                        last_name=rows["lname"],
                        email=rows["email"],
                        contract=rows["contract"],
                        schedule=rows["schedule"],
                        )
                        teacher.save()
                        
        row = ScheduleList.objects.get(email=request.user.email)
        rows = Teacher.objects.all().filter(schedule_id=row.schedules[-1])

        return render(request, self.template_name, {"rows": rows})
        
