from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Question, Answer
from django.urls import reverse_lazy
from .forms import QuestionCreateForm, AnswerCreateForm
# read about django anonymous user
# do not allow user to like his own answer
# use default names to avoid template_name
# no need for ans detail and ans list?
# def get_query_set
#   return model.objects.filter(user=self.request.user)


class HomeView(TemplateView):  # LoginRequiredMixin,
    template_name = 'FeQta/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        num = 555
        demo_data = [1000, 2000, 3000, 4000]
        context = {
            "num": num,
            "demo_data": demo_data
        }
        return context


class TopicListView(ListView):
    context_object_name = 'topics'

    def get_queryset(self):
        return Topic.objects.all()


class TopicDetailView(DetailView):
    model = Topic


class TopicCreateView(CreateView):
    model = Topic
    fields = ['name', 'desc', 'topic_logo']
    # success_url = reverse_lazy('home')


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    login_url = reverse_lazy('FeQta:login')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(QuestionCreateView, self).form_valid(form)


class QuestionDetailView(DetailView):
    model = Question

    def get_query_set(self):
        return Question.objects.filter(user=self.request.user)
    # slug_url_kwarg = 'slug2'


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    login_url = reverse_lazy('FeQta:login')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(AnswerCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AnswerCreateView, self).get_form_kwargs()
        # self.question = Question.objects.filter(slug=self.slug_url_kwarg)
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(*args, **kwargs)
        context['head'] = 'Write answer'
        context['title'] = 'Create-Answer'
        return context


class AnswerUpdateView(LoginRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerCreateForm
    login_url = reverse_lazy('FeQta:login')

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerUpdateView, self).get_context_data(*args, **kwargs)
        context['head'] = 'Update your answer'
        context['title'] = 'Update-answer'
        return context


class AnswersView(ListView):
    template_name = 'FeQta/answers.html'
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Question.objects.all()  # filter(owner=self.request.user)
        return qs


class RanksView(TemplateView):
    template_name = 'FeQta/ranks.html'


class ProfileView(TemplateView):
    template_name = 'FeQta/profile.html'




# notes
# from django.contrib.auth.decorators import login_required
# for FBV
# from django.views.generic import View
# def question_create_view(request):
#     form = QuestionCreateForm(request.POST or None)
#     errors = None
#
#     if form.is_valid():
#         if request.is_authenticated():
#             instance = form.save(commit=False)
#             # customize
#             # like pre save
#             instance.owner = request.user
#             instance.save()
#             return HttpResponseRedirect('/home/')
#         else:
#             return HttpResponseRedirect('/login/')
#
#     if form.errors:
#         errors = form.errors
#
#     template_name = 'FeQta/question_form.html'
#     context = {
#         "form":form,
#          "errors":errors
#     }
#     return render(request,template_name,context)
