from django.shortcuts import render
from django.views import generic
# from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView  # ,UpdateView,DeleteView
# from django.http import HttpResponse
from .models import Topic
from django.urls import reverse_lazy


class HomeView(TemplateView):
    template_name = 'FeQta/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        num = 555
        demo_data = [1000, 2000 , 3000, 4000]
        context = {
            "num": num,
            "demo_data": demo_data
        }
        return context


class TopicListView(generic.ListView):
    template_name = 'FeQta/topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.all()


class TopicDetailView(generic.DetailView):
    template_name = 'FeQta/topic_detail.html'
    model = Topic


class TopicCreateView(CreateView):
    model = Topic
    fields = ['name', 'desc', 'topic_logo']
    success_url = reverse_lazy('home')


class AnswersView(TemplateView):
    template_name = 'answers.html'


class RanksView(TemplateView):
    template_name = 'ranks.html'


class ProfileView(TemplateView):
    template_name = 'profile.html'


class GetStartedView(TemplateView):
    template_name = 'get_started.html'


