from django.shortcuts import render

from django.views.generic import TemplateView

class CalendarView(TemplateView):
        """
        A view that allows the user to see the teachers in a calendar
        """

        @staticmethod
        def calendar_name(name, role):
                return name, '-', role
        
        @staticmethod
        def get_teachers(day, teachers):
                return teachers[day*5:day*5 + 5]
        
        def get(self, request):
                print("yrdy")
                teachers_list = [['John', 'Cafeteria'], ['Rex', 'Weight Room'], ['Wasif', 'Library'], ['Karan', 'Bleachers'], ['Eric', 'Rover']]
                test = 'happy' #(calendar_name[get_teachers(1, teachers_list)[0]])
                return render(request, "calendar.html", {"day":1, "test":test})