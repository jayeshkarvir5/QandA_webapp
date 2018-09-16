from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.urls import reverse
# read docs for fields

User = settings.AUTH_USER_MODEL


class ProfileManager(models.Manager):

    def toggle_follow(self, request_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = request_user
        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            profile_.followers.add(user)
            is_following = True
        return profile_, is_following


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # user.profile
    # user.followers user.following
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)
    # following = models.ManyToManyField(User, related_name='following', blank=True)
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('FeQta:profile_detail', kwargs={'username': self.user.username})


def post_save_user_receiver(sender, instance, created, *args, **kwargs):

    if created:
        profile, is_created = Profile.objects.get_or_create(user=instance)
        default_user_profile = Profile.objects.get_or_create(user__username="FeQtA").first()  # user__username=
        default_user_profile.followers.add(instance)
        profile.followers.add(default_user_profile.user)


post_save.connect(post_save_user_receiver, sender=User)


class TopicQuerySet(models.query.QuerySet):

    def search(self, query):
        query = query.strip()
        if query:
            return self.filter(
                    Q(name__icontains=query) |
                    Q(name__iexact=query)
                ).distinct()
        return self


class TopicManager(models.Manager):

    def get_queryset(self):
        return TopicQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Topic(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, blank=True)
    followers = models.ManyToManyField(User, related_name='topics_followed', blank=True)
    topic_logo = models.FileField()
    slug = models.SlugField(null=True, blank=True)
    objects = TopicManager()

    def __str__(self):
        return self.name + '-' + self.desc

    def get_absolute_url(self):
        return reverse('FeQta:topic_detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return self.name


def slug_pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_pre_save_receiver, Topic)


class QuestionQuerySet(models.query.QuerySet):

    def search(self, query):
        query = query.strip()  # get rid of preciding space
        if query:  # Question.objects.all().search(query) #Question.objects.filter(something).search()
            return self.filter(
                    Q(question__icontains=query) |
                    Q(topic__name__icontains=query)
                ).distinct()
        return self


class QuestionManager(models.Manager):

    def get_queryset(self):
        return QuestionQuerySet(self.model, using=self._db)

    def search(self, query):  # Question.objects.search()
        return self.get_queryset().search(query)


class Question(models.Model):
    # what if account is deleted
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.TextField()
    desc = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='question_followed_by', blank=True)
    objects = QuestionManager()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('FeQta:question_detail', kwargs={'slug': self.slug})
    #   return reverse('FeQta:question_detail', kwargs={'slug1':self.topic.slug, 'slug2': self.slug})

    def __str__(self):
        return self.question

    @property
    def title(self):
        return "question-by" + self.owner.username + str(self.pk)


pre_save.connect(slug_pre_save_receiver, Question)


class Answer(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField(max_length=20000)
    likes = models.ManyToManyField(User, related_name='answers_liked', blank=True)
    needs_improvement = models.ManyToManyField(User, related_name='answers_needimp', blank=True)
    dislikes = models.ManyToManyField(User, related_name='answers_disliked', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['-updated', '-timestamp']

    def __str__(self):
        return self.question.question + " answered by " + self.owner.username

    def get_absolute_url(self):
        return reverse('FeQta:answer_detail', kwargs={'slug': self.slug})

    @property
    def title(self):
        return "answer-to"+ str(self.question.pk) + "by" + self.owner.username


pre_save.connect(slug_pre_save_receiver, Answer)


# contents = models.Textfield(help_text="Seperate by comma")
# def get_contents(self):
#   return self.contents.split(',')

# class Comment(models.Model):
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     text = models.CharField(max_length=700)
#     #add reply button
#
#
# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     text = models.CharField(max_length=700)
#     #add reply button
#
# class User
