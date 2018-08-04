from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .models import Topic


class HomeListView(generic.ListView):
    template_name = 'FeQta/home.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.all()


class TopicDetailView(generic.DetailView):
    template_name = 'FeQta/topic_detail.html'
    model = Topic


class AnswersView(TemplateView):
    template_name = 'answers.html'


class RanksView(TemplateView):
    template_name = 'ranks.html'


class ProfileView(TemplateView):
    template_name = 'profile.html'


class GetStartedView(TemplateView):
    template_name = 'get_started.html'


# class HomeView(TemplateView):
#     template_name = 'home.html'
#     def get_context_data(self, *args, **kwargs):
#         context = super(HomeView,self).get_context_data(*args, **kwargs)
#         num = None
#         demo_data = [
#             random.randint(0, 1000),
#             random.randint(0, 1000),
#             random.randint(0, 1000),
#             random.randint(0, 1000),
#         ]
#         bol_var = True
#         if bol_var:
#             num = 9091
#         context = {
#             "num":num,
#             "demo_data":demo_data
#         }
#         return context
