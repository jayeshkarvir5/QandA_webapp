from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Topic, Question, Answer, Profile
from django.urls import reverse_lazy, reverse
from .forms import QuestionCreateForm, AnswerCreateForm
from django.db.models import Q
# read about django anonymous user
# do not allow user to like his own answer
# use default names to avoid template_name
# no need for ans detail and ans list?
# take care of user changing the url
# use &nbsp; for spaces
# def get_query_set
#   return model.objects.filter(user=self.request.user)
# provide update button in profile for answers
# work on answer views and comment views
# login needs to be fixed


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
    def get_context_data(self, *args, **kwargs):
        context = super(TopicDetailView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        topic = self.object
        count = topic.followers.all().count()
        context['count'] = count
        is_following = False
        if user in topic.followers.all():
            is_following = True
        context['is_following'] = is_following
        return context


def TopicFollowToggle(request, slug):
    user = request.user
    topic_to_toggle = Topic.objects.get(slug=slug)
    if user in topic_to_toggle.followers.all():
        topic_to_toggle.followers.remove(user)
    else:
        topic_to_toggle.followers.add(user)
    topic_to_toggle.save()
    return redirect(f'/FeQta/topics/{topic_to_toggle.slug}/')


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

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        question = self.object
        count = question.followers.all().count()
        context['count'] = count
        is_following = False
        if user.is_authenticated:
            ans_cond = False  # not answered
            ans = Answer.objects.filter(question=question, owner=user).first()
            if ans:
                ans_cond = True
                context['ans'] = ans
            context['ans_cond'] = ans_cond
        if user in question.followers.all():
                is_following = True
        context['is_following'] = is_following
        return context

    # slug_url_kwarg = 'slug2'


def QuestionFollowToggle(request, slug):
    user = request.user
    question_to_toggle = Question.objects.get(slug=slug)
    if user in question_to_toggle.followers.all():
        question_to_toggle.followers.remove(user)
    else:
        question_to_toggle.followers.add(user)
    question_to_toggle.save()
    return redirect(f'/FeQta/question/{question_to_toggle.slug}/')


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
            return super(AnswerUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerUpdateView, self).get_context_data(*args, **kwargs)
        context['head'] = 'Update your answer'
        context['title'] = 'Update-answer'
        return context


def LikeToggle(request, slug):
    user = request.user
    answer_to_toggle = Answer.objects.get(slug=slug)
    if user in answer_to_toggle.likes.all():
        answer_to_toggle.likes.remove(user)
    else:
        answer_to_toggle.likes.add(user)
        answer_to_toggle.save()
    return redirect(f'/FeQta/answer/{answer_to_toggle.slug}/')


def NeedimpToggle(request, slug):
    user = request.user
    answer_to_toggle = Answer.objects.get(slug=slug)
    if user in answer_to_toggle.needs_improvement.all():
        answer_to_toggle.needs_improvement.remove(user)
    else:
        answer_to_toggle.needs_improvement.add(user)
        answer_to_toggle.save()
    return redirect(f'/FeQta/answer/{answer_to_toggle.slug}/')


def DislikeToggle(request, slug):
    user = request.user
    answer_to_toggle = Answer.objects.get(slug=slug)
    if user in answer_to_toggle.dislikes.all():
        answer_to_toggle.dislikes.remove(user)
    else:
        answer_to_toggle.dislikes.add(user)
        answer_to_toggle.save()
    return redirect(f'/FeQta/answer/{answer_to_toggle.slug}/')


class AnswerDetailView(DetailView):
    model = Answer
    def get_context_data(self, *args, **kwargs):
        context = super(AnswerDetailView, self).get_context_data(*args, **kwargs)
        is_liked = False
        is_need_imp = False
        is_disliked = False
        user = self.request.user
        answer = self.object
        if user in answer.likes.all():
            is_liked = True
        if user in answer.needs_improvement.all():
            is_need_imp = True
        if user in answer.dislikes.all():
            is_disliked = True
        context['is_liked'] = is_liked
        context['is_need_imp'] = is_need_imp
        context['is_disliked'] = is_disliked
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
        if self.request.user.is_authenticated:
            is_following = False
            if user.profile in self.request.user.is_following.all():
                is_following = True
            context['is_following'] = is_following
        query = self.request.GET.get('q')
        qs = Question.objects.filter(owner=user)  # user.question_set.all().count()
        qs2 = Answer.objects.filter(owner=user)  # user.answer_set.all().count()
        qs3 = user.topics_followed.all()  # Topic.objects.filter(followers=user)
        context['count'] = user.profile.followers.all().count()
        context['count1'] = qs.count()
        context['count2'] = qs2.count()
        context['count3'] = qs3.count()
        context['count4'] = user.answers_liked.all().count()
        context['count5'] = user.answers_needimp.all().count()
        context['count6'] = user.answers_disliked.all().count()
        if query:
            qs = qs.search(query)  # only owner=user questions
            # qs = Question.objects.search(query) all questions
            qs3 = qs3.search(query)
        if qs:
            context['questions'] = qs
        if qs2:
            context['answers'] = qs2
        if qs3:
            context['topics'] = qs3
        return context


class ProfileFollowToggle(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/FeQta/profile/{profile_.user.username}/")


class SearchListView(TemplateView):
    template_name = "FeQta/search.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = Question.objects.search(query)  # all questions
            qs1 = Topic.objects.search(query)
            qs2 = User.objects.filter(
                Q(username__icontains=query) |
                Q(username__iexact=query)
            )
            context['questions'] = qs
            context['topics'] = qs1
            context['users'] = qs2
        return context


# class LoginView(LoginRequiredMixin, TemplateView):
#     template_name = "FeQta/home.html"
#     login_url = reverse_lazy('FeQta:login')


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
