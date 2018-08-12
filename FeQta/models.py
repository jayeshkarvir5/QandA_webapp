from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
# read docs for fields

User = settings.AUTH_USER_MODEL


class Topic(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    topic_logo = models.FileField()
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name + '-' + self.desc

    @property
    def title(self):
        return self.name


def topic_pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(topic_pre_save_receiver, Topic)


class Question(models.Model):
    owner =  models.ForeignKey(User, on_delete=models.CASCADE)
    # what is account is deleted
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    desc = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=20000)
    likes = models.IntegerField()
    needs_improvement = models.IntegerField()
    dislikes = models.IntegerField()


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
