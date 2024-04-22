from django.views.generic import TemplateView
from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
import csv

from core.models import Schedule, ScheduleList, Teacher

class GenerateView(TemplateView):
    """
     A view for the generate page form.
    """
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

        # retrieve data from form
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

        schedule.save() #save schedule
        # a check to save the id of the schedules created
        check = ScheduleList.objects.filter(email=request.user.email).values()
        if len(check) == 0:
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
     A view for the teachers page form.
    """
    template_name = "teachers.html"

    def get(self, request):
        """
        Gets user information and authenticates it
            Args: 
                request (data): the request of the get function containing the form data.
            Returns:
                (Http response)
        """
        row = ScheduleList.objects.get(email=request.user.email)
        rows = Teacher.objects.all().filter(schedule_id=row.schedules[-1])

        return render(request, self.template_name, {"rows": rows})

    def post(self, request):
        """
        Gets user information and authenticates it
            Args: 
                request (data): the request of the post function containing the form data.
            Returns:
                (Http response)
        """
        if "contract" in request.POST:
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
        else:
               
                 
                row = ScheduleList.objects.get(email=request.user.email)
               # ifile = open(request.FILES["teachersx"], "rt", encoding="utf8")
                ifile = request.FILES["teachersx"]
                decoded_file = ifile.read().decode('utf-8').splitlines()
                data  = csv.DictReader(decoded_file)

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
                # for rows in data:
                #         print(rows)
                #         teacher = Teacher(
                #         schedule_id=row.schedules[-1],
                #         first_name=rows[0],
                #         last_name=rows[1],
                #         email=rows[2],
                #         contract=rows[3],
                #         schedule=rows[4],
                #         )
                #         teacher.save()


        
        row = ScheduleList.objects.get(email=request.user.email)
        rows = Teacher.objects.all().filter(schedule_id=row.schedules[-1])

        return render(request, self.template_name, {"rows": rows})
        
