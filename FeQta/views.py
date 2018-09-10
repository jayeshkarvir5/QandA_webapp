from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Topic, Question, Answer
from django.urls import reverse_lazy, reverse
from .forms import QuestionCreateForm, AnswerCreateForm
# read about django anonymous user
# do not allow user to like his own answer
# use default names to avoid template_name
# no need for ans detail and ans list?
# take care of user updating from url
# use &nbsp; for spaces
# def get_query_set
#   return model.objects.filter(user=self.request.user)
# provide update button in profile for answers


User = get_user_model()


class HomeView(TemplateView):  # LoginRequiredMixin,
    template_name = 'FeQta/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        num = 555
        demo_data = [1000, 2000, 3000, 4000]
        context = {
            "num": num,
            "demo_data": demo_data,
            "error": None,
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
        try:
            # question = get_object_or_404(Question, slug=self.kwargs.get('slug'))
            question = Question.objects.get(slug=self.kwargs.get('slug'))
        except Question.DoesNotExist:
            return HttpResponse('<h3>Question not found</h3>')
        instance.question = question
        if instance.owner == instance.question.owner:
            return HttpResponse('<h3>User is answering the question they asked</h3>')
        else:
            return super(AnswerCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AnswerCreateView, self).get_form_kwargs()
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

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.owner != self.request.user:
            return HttpResponse('<h3>Cannot edit as you have not answered this question</h3>')
        else:
            return super(AnswerCreateView, self).form_valid(form)

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


class ProfileDetailView(DetailView):
    template_name = 'FeQta/profile_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        query = self.request.GET.get('q')
        qs = Question.objects.filter(owner=user)
        qs2 = Answer.objects.filter(owner=user)
        if query:
            qs = qs.search(query) # only owner=user questions
            # qs = Question.objects.search(query) all questions
        if qs:
            context['questions'] = qs
        if qs2:
            context['answers'] = qs2
        return context


class SearchListView(ListView):
    template_name = "FeQta/search.html"
    context_object_name = 'topics'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Topic.objects.search(query)
        return None

    def get_context_data(self, *args, **kwargs):
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = Question.objects.search(query)  # all questions
            # qs2 = User.objects.search(query)
            qs2 = User.objects.all()
            context['questions'] = qs
            context['users'] = qs2
        return context


class RanksView(TemplateView):
    template_name = 'FeQta/ranks.html'


class ProfileView(TemplateView):
    template_name = 'FeQta/profile.html'




# notes
# from django.contrib.auth.decorators import login_required
# for FBV
# from django.views.generic import View

# def get_initial(self):
#     question = get_object_or_404(Question, slug=self.kwargs.get('slug'))
#     question = Question.objects.filter(slug=self.kwargs.get('slug'))
#     return {
#         'question': question,
#     }

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
