from django.shortcuts import render

from django.views.generic import TemplateView
import datetime
from calendar import monthrange


class CalendarView(TemplateView):
    """
    A view that allows the user to see the teachers in a calendar
    """

    @staticmethod
    def generate_calendar(day, month, year):
        calendar_string = '<tr class="text-left align-top">'
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
        day_name = datetime.date(year, month, day).weekday()
        empty_days = (day_name + 1) % 7
        iterator = 1
        max_days = monthrange(year, month)

        for x in range(empty_days):
            calendar_string += ' <td class="h-24 border bg-gray-50 px-2"></td>'
        for y in range(7 - empty_days):
            calendar_string += f' <td class="h-24 border px-2">{iterator}</td>'
            iterator += 1

        calendar_string += " </tr>"

        for i in range(5):
            if iterator > max_days[1]:
                continue
            calendar_string += ' <tr class="text-left align-top">'
            for k in range(7):
                if iterator <= max_days[1]:
                    calendar_string += f' <td class="h-24 border px-2">{iterator}</td>'
                else:
                    calendar_string += ' <td class="h-24 border bg-gray-50 px-2"></td>'
                iterator += 1
            calendar_string += " </tr>"
        calendar_name = f"{month_name[month]} {year}"
        return calendar_string, calendar_name

    def get(self, request):
        year = 2024
        month = 9
        day = 1
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

        print("yrdy")
        teachers_list = [
            ["John", "Cafeteria"],
            ["Rex", "Weight Room"],
            ["Wasif", "Library"],
            ["Karan", "Bleachers"],
            ["Eric", "Rover"],
        ]
        test = '<p class="font-bold">happy</p> <p class="font-bold">happy</p>'  # (calendar_name[get_teachers(1, teachers_list)[0]])
        return render(
            request,
            "calendar.html",
            {
                "day": 1,
                "test": test,
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

    @staticmethod
    def calendar_name(name, role):
        return name, "-", role

    @staticmethod
    def get_teachers(day, teachers):
        return teachers[day * 5 : day * 5 + 5]
