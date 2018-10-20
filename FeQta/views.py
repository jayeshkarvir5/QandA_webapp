from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, logout
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Topic, Question, Answer, Profile
from django.urls import reverse_lazy, reverse
from .forms import QuestionCreateForm, AnswerCreateForm, RegisterForm, ProfileUpdateForm
from django.db.models import Q
# read about django anonymous user
# take care of user changing the url
# use &nbsp; for spaces
# work on answer views(delete,update), question(delete?) and comment views?
# login needs to be fixed
# create a counter based html temp to render mixed queries of different qs
# activate user

User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('FeQta:login')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('FeQta:logout_page')
        return super(RegisterView, self).dispatch(*args, **kwargs)


def LogoutView(request):
    logout(request)
    return redirect('/FeQta/login/')


class LogoutPage(TemplateView):
    template_name = 'FeQta/logout_page.html'


class HomeView(View):
    # create a counter based html temp to render mixed queries of different qs
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            qs = Answer.objects.all()
            return render(request,'FeQta/home.html',{'qs':qs})
        user = request.user
        is_following_user_ids =[x.user.id for x in user.is_following.all()]
        is_following_topic_id =[x.id for x in user.topics_followed.all()]
        followed_questions = user.question_followed_by.all()
        qs = Answer.objects.filter(question__in=followed_questions)  # followed question answered,
        qs1 = Answer.objects.filter(question__owner__id=user.id)  # answer for my question
        qs2 = Answer.objects.filter(owner__id__in=is_following_user_ids)  # following_user answer
        qs3 = Answer.objects.filter(likes__id__in=is_following_user_ids, question__topic__in=is_following_topic_id)  # like by following_user
        qs4 = Answer.objects.filter(question__topic__in=is_following_topic_id)  # topics followed answers
        # qs5 = Answer.objects.filter(question__owner__id__in=is_following_user_ids)  # following_user ques answered
        context = {
            "ans_followed_questions": qs,
            "ans_my_ques": qs1,
            "ans_following_user": qs2,
            "likes": qs3,
            "topic_rld": qs4,
            "is_following_user_ids": is_following_user_ids,
        }
        return render(request,'FeQta/home_feed.html',context)


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
    profile = Profile.objects.filter(user=question_to_toggle.owner)[0]
    if user in question_to_toggle.followers.all():
        question_to_toggle.followers.remove(user)
        profile.score -= 1
    else:
        question_to_toggle.followers.add(user)
        profile.score += 1
    question_to_toggle.save()
    profile.save()
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
            return render(self.request, 'FeQta/error_page.html', {'error': "Question not found"})
        instance.question = question
        if instance.owner == instance.question.owner:
            return render(self.request, 'FeQta/error_page.html', {'error': "User is answering the question they asked"})
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
            return render(self.request, 'FeQta/error_page.html', {'error': "Only the owner of this answer may edit."})
        else:
            return super(AnswerUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerUpdateView, self).get_context_data(*args, **kwargs)
        context['head'] = 'Update your answer'
        context['title'] = 'Update-answer'
        return context


class AnswerDeleteView(LoginRequiredMixin, DeleteView):
    model = Answer
    login_url = reverse_lazy('FeQta:login')
    success_url = reverse_lazy('FeQta:delete_success')

    def get_object(self, queryset=None):
        obj = super(AnswerDeleteView, self).get_object()
        if not obj.owner == self.request.user:
            return render(self.request, 'FeQta/error_page.html', {'error': "Only the owner of this answer may delete it."})
        return obj


class AnswerDeletePage(LoginRequiredMixin,TemplateView):
    template_name = 'FeQta/delete_answer_page.html'


class AnswerDeleteSuccess(LoginRequiredMixin,TemplateView):
    template_name = 'FeQta/delete_success.html'


def LikeToggle(request, slug):
    user = request.user
    answer_to_toggle = Answer.objects.get(slug=slug)
    owner = answer_to_toggle.owner
    profile = Profile.objects.filter(user=owner)[0]
    if user in answer_to_toggle.likes.all():
        answer_to_toggle.likes.remove(user)
        profile.score -= 2
    else:
        answer_to_toggle.likes.add(user)
        profile.score += 2
        answer_to_toggle.save()
    profile.save()
    return redirect(f'/FeQta/answer/{answer_to_toggle.slug}/')


def NeedimpToggle(request, slug):
    user = request.user
    answer_to_toggle = Answer.objects.get(slug=slug)
    owner = answer_to_toggle.owner
    profile = Profile.objects.filter(user=owner)[0]
    if user in answer_to_toggle.needs_improvement.all():
        answer_to_toggle.needs_improvement.remove(user)
        profile.score -= 1
    else:
        answer_to_toggle.needs_improvement.add(user)
        profile.score += 1
        answer_to_toggle.save()
    profile.save()
    return redirect(f'/FeQta/answer/{answer_to_toggle.slug}/')


def DislikeToggle(request, slug):
    user = request.user
    answer_to_toggle = Answer.objects.get(slug=slug)
    owner = answer_to_toggle.owner
    profile = Profile.objects.filter(user=owner)[0]
    if user in answer_to_toggle.dislikes.all():
        answer_to_toggle.dislikes.remove(user)
        profile.score += 1
    else:
        answer_to_toggle.dislikes.add(user)
        profile.score -= 1
        answer_to_toggle.save()
    profile.save()
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
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            qs = Question.objects.all()
            return render(request, 'FeQta/answers.html', {'qs':qs})
        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        is_following_topic_id = [x.id for x in user.topics_followed.all()]
        qs1 = Question.objects.filter(owner__id__in=is_following_user_ids, topic__in=is_following_topic_id)  # following_user ques
        qs2 = Question.objects.filter(topic__in=is_following_topic_id)  # topics followed ques
        context = {
            "topic_rld": qs2,
            "following_user": qs1,
        }
        return render(request, 'FeQta/answers_loggedin.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "FeQta/profile_form.html"
    login_url = reverse_lazy('FeQta:login')

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise 404
            # return render(self.request, 'FeQta/error_page.html', {'error': "Question not found"})
        return get_object_or_404(Profile, user__username__iexact=username)

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.user != self.request.user:
            return render(self.request, 'FeQta/error_page.html', {'error': "Only the owner of this Profile may edit."})
        else:
            return super(ProfileUpdateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
        context['head'] = 'Update your Profile'
        context['title'] = ''
        return context


class ProfileDetailView(DetailView):
    template_name = 'FeQta/profile_detail.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username is None:
            raise 404
            # return render(self.request, 'FeQta/error_page.html', {'error': "Question not found"})
        return get_object_or_404(Profile, user__username__iexact=username)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = self.object.user
        print(user)
        print(self.request.user)
        if self.request.user.is_authenticated:
            if user.is_authenticated:
                is_following = False
            if user.profile in self.request.user.is_following.all():
                is_following = True
            context['is_following'] = is_following
        query = self.request.GET.get('q')
        qs = Question.objects.filter(owner=user)  # user.question_set.all().count()
        qs2 = Answer.objects.filter(owner=user)  # user.answer_set.all().count()
        qs3 = user.topics_followed.all()  # Topic.objects.filter(followers=user)
        context['count'] = user.profile.followers.all().count()
        context['count0'] = user.is_following.all().count()
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


class RanksView(TemplateView):
    template_name = 'FeQta/ranks.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RanksView, self).get_context_data(*args, **kwargs)
        qs = Profile.objects.all()
        # for itr in qs:
        #     ques = Question.objects.filter(owner=itr.user)
        #     itr.score = 0
        #     for que in ques:
        #         itr.score += que.followers.all().count()
        #     answers = Answer.objects.filter(owner=itr.user)
        #     for ans in answers:
        #         itr.score += 2*ans.likes.count() + ans.needs_improvement.count() - ans.dislikes.count()
        #     itr.score += itr.followers.count()
        #     itr.save()
        # qs = Profile.objects.all()
        context['profiles'] = qs
        context['total'] = qs.count()
        return context
