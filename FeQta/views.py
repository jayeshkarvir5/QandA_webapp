from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
import random
from django.http import HttpResponse


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView,self).get_context_data(*args, **kwargs)
        num = None
        demo_data = [
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
            random.randint(0, 1000),
        ]
        bol_var = True
        if bol_var:
            num = 9091
        context = {
            "num":num,
            "demo_data":demo_data
        }
        return context

class AnswersView(TemplateView):
    template_name = 'answers.html'

class RanksView(TemplateView):
    template_name = 'ranks.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class Get_StartedView(TemplateView):
    template_name = 'get_started.html'