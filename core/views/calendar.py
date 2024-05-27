"""
calendar.py
ICS4U SDP 
Muhammad Wasif Kamran, Karan Chawla, Eric Sui 
CBV related to calendar generation and display 
"""
# Django imports
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import FileResponse
from core.models import Teacher, ScheduleList

# Other Python imports for CSV and ICS handling as well as calendar manipulations
import random
import datetime
from calendar import monthrange
from ics import Calendar, Event
import csv


class ScheduleTeacher:
    """
    Class to represent a teacher in the schedule
    Attributes:
        name: str
        schedule: schedule (Django model)
        dor: int (Degree of Restrictiveness)
        potential: list[int]
    """

    def __init__(self, name: str, schedule: list[list[str]]) -> None:
        """
        Initializes instance attributes
        Args:
            name: str
            schedule: list[list[str]]
        """
        # Assign values to attributes
        self.name = name
        self.schedule = schedule
        self.dor: int = 0
        self.potential: list[int] = []
        # If no predefined schedule, set these ones (handles edge cases)
        if len(schedule[0]) == 0:
            self.schedule[0] = [
                random.choice(["TAKEN", "SPARE"]),
                random.choice(["TAKEN", "SPARE"]),
                random.choice(["TAKEN", "SPARE"]),
                random.choice(["TAKEN", "SPARE"]),
            ]

            self.schedule[1] = [
                random.choice(["TAKEN", "SPARE"]),
                random.choice(["TAKEN", "SPARE"]),
                random.choice(["TAKEN", "SPARE"]),
                random.choice(["TAKEN", "SPARE"]),
            ]
            self.schedule[2] = [
                self.schedule[0][1],
                self.schedule[0][0],
                self.schedule[0][3],
                self.schedule[0][2],
            ]
            self.schedule[3] = [
                self.schedule[1][1],
                self.schedule[1][0],
                self.schedule[1][3],
                self.schedule[1][2],
            ]


# global_iterator goes over all the days in the year
global_iterator = 0
# constructed calendar is represented by a 2D list
construction: list[list[str]] = [[], [], [], [], [], [], [], [], [], [], [], []]


class CalendarView(TemplateView):
    """
    CBV for the calendar page
    """

    # Define construction as global
    global construction

    @staticmethod
    def construct_days(email):
        """
        Construct the teachers in a certain day period which will cycle over the year
        Args:
            email (str)
        Returns:
            None
        """
        # Read in list of teachers from database
        teachers: list[ScheduleTeacher] = []
        row = ScheduleList.objects.get(email=email)
        rows = Teacher.objects.all().filter(schedule_id=row.schedules[-1])

        # Map a teacher to an index so that they can be accessed from the teachers list
        teacher_index_map = {}
        for i in range(0, len(rows)):
            # Parse schedule
            schedule_string = rows[i].schedule
            schedule_list = schedule_string.split("/")
            # Split into the days
            day1 = [
                schedule_list[0],
                schedule_list[1],
                schedule_list[2],
                schedule_list[3],
            ]
            day2 = [
                schedule_list[4],
                schedule_list[5],
                schedule_list[6],
                schedule_list[7],
            ]
            day3 = [
                schedule_list[1],
                schedule_list[0],
                schedule_list[3],
                schedule_list[2],
            ]
            day4 = [
                schedule_list[5],
                schedule_list[4],
                schedule_list[7],
                schedule_list[6],
            ]
            # Instantiate object and append to the list (also save the index at which the teacher is in the list)
            cur = ScheduleTeacher(
                rows[i].first_name + rows[i].last_name, [day1, day2, day3, day4]
            )
            teachers.append(cur)
            teacher_index_map[rows[i].first_name + rows[i].last_name] = i

        # Candidates for every day in a 12 day cycle
        candidates: list[list[str]] = [[], [], [], [], [], [], [], [], [], [], [], []]
        # For every teacher, if they have a spare before or after lunch, they are a possible candidate on that day
        for teacher in teachers:
            for day in range(0, 4):
                if (
                    teacher.schedule[day][1] == "SPARE"
                    or teacher.schedule[day][2] == "SPARE"
                ):
                    candidates[day].append(teacher.name)

                    candidates[day + 4].append(teacher.name)

                    candidates[day + 8].append(teacher.name)

                    teacher.potential.append(day)
                    teacher.potential.append(day + 4)
                    teacher.potential.append(day + 8)

        # Create a list of degrees of restrictiveness which says how restricted a teacher is (the less  restricted, the higher the dor)
        dors: list[int] = []
        for i in range(len(teachers)):
            dors.append(0)
        for teacher in teachers:
            for cur_day in candidates:
                if teacher.name in cur_day:
                    dors[teacher_index_map[teacher.name]] += 1

        # Sort the teachers by ascending dor (most to least restricted)
        for teacher in teachers:
            teacher.dor = dors[teacher_index_map[teacher.name]]
        sorted_teachers = sorted(teachers, key=lambda x: x.dor)

        # Fill in the teachers that are the most restricted and keep going until all teachers or spots are filled in
        for teacher in sorted_teachers:
            if teacher.dor == 0 or len(teacher.potential) == 0:
                continue
            # Randomly fill in slots till they make a valid schedule
            choice = random.choice(teacher.potential)
            while len(construction[choice]) == 6:
                choice = random.choice(teacher.potential)

            construction[choice].append(teacher.name)

            if len(construction[choice]) == 6:
                for alt_teacher in sorted_teachers:
                    if choice in alt_teacher.potential:
                        alt_teacher.potential.remove(choice)

    # Global var to store where the teachers are going to be placed for the calendar
    global data
    data = [("Date", "Name")]

    # Resource: https://docs.djangoproject.com/en/5.0/ref/templates/builtins/

    @staticmethod
    def generate_calendar(day, month, year):
        """
        Generates a calendar template for a given month
        Args:
            day: str
            month: str
            year: str
        Returns:
            str, str
        Note: code might seem complex, but its really just writing HTML code to be injected
        """
        # Creating a template string for what should be displayed on the frontend
        calendar_string = '<tr class="text-left align-text-top">'
        month_name = [
            "Unknown",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        # Using the datetime library to set up the weekday counting mechanism (to determine if its a monday, tuesday, etc)
        day_name = datetime.date(year, month, day).weekday()
        empty_days = (day_name + 1) % 7
        iterator = 1
        global global_iterator
        max_days = monthrange(year, month)

        # Resource: https://icspy.readthedocs.io/en/stable/

        global c
        c = Calendar()

        # Setting days at the end of the month that should be blank to be blank using tailwind.
        for x in range(empty_days):
            calendar_string += ' <td class="h-24 border bg-gray-50 px-2"></td>'
        for y in range(7 - empty_days):
            if datetime.date(year, month, iterator).weekday() <= 4:
                current = construction[global_iterator % 12]
                calendar_string += f' <td class="h-24 border align-text-top px-2 py-1">{iterator} <br><br> {current[0]} <br> {current[1]} <br> {current[2]} <br> {current[3]} <br> {current[4]} <br> {current[5]}</td>'
                global_iterator += 1

                # Add events to the ICS file
                e1 = Event()
                e1.name = current[0]
                e1.begin = datetime.date(year, month, iterator)
                e2 = Event()
                e2.name = current[0]
                e2.begin = datetime.date(year, month, iterator)
                e3 = Event()
                e3.name = current[0]
                e3.begin = datetime.date(year, month, iterator)
                e4 = Event()
                e4.name = current[0]
                e4.begin = datetime.date(year, month, iterator)
                e5 = Event()
                e5.name = current[0]
                e5.begin = datetime.date(year, month, iterator)
                e6 = Event()
                e6.name = current[0]
                e6.begin = datetime.date(year, month, iterator)

                c.events.add(e1)
                c.events.add(e2)
                c.events.add(e3)
                c.events.add(e4)
                c.events.add(e5)
                c.events.add(e6)
                data.append((f"{month}/{iterator}", f"{current[0]}"))
                data.append((f"{month}/{iterator}", f"{current[1]}"))
                data.append((f"{month}/{iterator}", f"{current[2]}"))
                data.append((f"{month}/{iterator}", f"{current[3]}"))
                data.append((f"{month}/{iterator}", f"{current[4]}"))
                data.append((f"{month}/{iterator}", f"{current[5]}"))
            else:
                calendar_string += f' <td class="h-24 border align-text-top px-2 py-1">{iterator}<br><br><br><br><br><br><br><br></td>'
            iterator += 1

        calendar_string += " </tr>"

        # Generating the HTML code to be injected
        for i in range(5):
            if iterator > max_days[1]:
                continue
            calendar_string += ' <tr class="text-left align-text-top">'
            for k in range(7):
                if iterator <= max_days[1]:
                    if datetime.date(year, month, iterator).weekday() <= 4:
                        current = construction[global_iterator % 12]
                        calendar_string += f' <td class="h-24 border align-text-top px-2 py-1">{iterator} <br><br> {current[0]} <br> {current[1]} <br> {current[2]} <br> {current[3]} <br> {current[4]} <br> {current[5]}</td>'
                        global_iterator += 1

                        e1 = Event()
                        e1.name = current[0]
                        e1.begin = datetime.date(year, month, iterator)
                        e2 = Event()
                        e2.name = current[0]
                        e2.begin = datetime.date(year, month, iterator)
                        e3 = Event()
                        e3.name = current[0]
                        e3.begin = datetime.date(year, month, iterator)
                        e4 = Event()
                        e4.name = current[0]
                        e4.begin = datetime.date(year, month, iterator)
                        e5 = Event()
                        e5.name = current[0]
                        e5.begin = datetime.date(year, month, iterator)
                        e6 = Event()
                        e6.name = current[0]
                        e6.begin = datetime.date(year, month, iterator)

                        c.events.add(e1)
                        c.events.add(e2)
                        c.events.add(e3)
                        c.events.add(e4)
                        c.events.add(e5)
                        c.events.add(e6)
                        data.append((f"{month}/{iterator}", f"{current[0]}"))
                        data.append((f"{month}/{iterator}", f"{current[1]}"))
                        data.append((f"{month}/{iterator}", f"{current[2]}"))
                        data.append((f"{month}/{iterator}", f"{current[3]}"))
                        data.append((f"{month}/{iterator}", f"{current[4]}"))
                        data.append((f"{month}/{iterator}", f"{current[5]}"))
                    else:
                        calendar_string += f' <td class="h-24 border align-text-top px-2 py-1">{iterator}<br><br><br><br><br><br><br><br></td>'
                else:
                    calendar_string += ' <td class="h-24 border bg-gray-50 px-2"></td>'
                iterator += 1
            calendar_string += " </tr>"

        # Getting the appropiate month name
        calendar_name = f"{month_name[month]} {year}"

        return calendar_string, calendar_name

    def post(self, request):
        """
        Handle POST request from the calendar
        Args:
            request: dict
        Returns:
            None
        """

        # Resource: https://nemecek.be/blog/165/django-how-to-let-user-download-a-file

        # If the POST request is related to the ICS file, write to the ICS file and download it
        if "ics" in request.POST:
            with open("my.ics", "w") as f:
                f.writelines(c.serialize_iter())
            return FileResponse(
                open("my.ics", "rb"), as_attachment=True, filename="supervision.ics"
            )

        # Reference: https://chat.openai.com/
        # If the POST request is related to the CSV file, write the CSV file and download it
        if "csv" in request.POST:
            with open("my.csv", "w", newline="") as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
            return FileResponse(
                open("my.csv", "rb"), as_attachment=True, filename="supervision.csv"
            )

    def get(self, request):
        """
        Handle GET requests from the calendar
        Args:
            request: dict
        Returns:
            HTML render
        """
        # Define the current school year
        year = 2024
        month = 9
        day = 1
        self.construct_days(request.user.email)
        # Generating strings for the calendar
        # TODO: Refactor this so it's more maintainable
        calendar_string1, calendar_name1 = self.generate_calendar(day, month, year)
        calendar_string2, calendar_name2 = self.generate_calendar(day, month + 1, year)
        calendar_string3, calendar_name3 = self.generate_calendar(day, month + 2, year)
        calendar_string4, calendar_name4 = self.generate_calendar(day, month + 3, year)
        calendar_string5, calendar_name5 = self.generate_calendar(
            day, month - 8, year + 1
        )
        calendar_string6, calendar_name6 = self.generate_calendar(
            day, month - 7, year + 1
        )
        calendar_string7, calendar_name7 = self.generate_calendar(
            day, month - 6, year + 1
        )
        calendar_string8, calendar_name8 = self.generate_calendar(
            day, month - 5, year + 1
        )
        calendar_string9, calendar_name9 = self.generate_calendar(
            day, month - 4, year + 1
        )
        calendar_string10, calendar_name10 = self.generate_calendar(
            day, month - 3, year + 1
        )

        return render(
            # Returning the calendar strings for the frontend
            request,
            "calendar.html",
            {
                "day": 1,
                "calendar_string1": calendar_string1,
                "calendar_name1": calendar_name1,
                "calendar_string2": calendar_string2,
                "calendar_name2": calendar_name2,
                "calendar_string3": calendar_string3,
                "calendar_name3": calendar_name3,
                "calendar_string4": calendar_string4,
                "calendar_name4": calendar_name4,
                "calendar_string5": calendar_string5,
                "calendar_name5": calendar_name5,
                "calendar_string6": calendar_string6,
                "calendar_name6": calendar_name6,
                "calendar_string7": calendar_string7,
                "calendar_name7": calendar_name7,
                "calendar_string8": calendar_string8,
                "calendar_name8": calendar_name8,
                "calendar_string9": calendar_string9,
                "calendar_name9": calendar_name9,
                "calendar_string10": calendar_string10,
                "calendar_name10": calendar_name10,
            },
        )
