from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    followers = models.IntegerField()
    album_logo = models.FileField()
    def __str__(self):
        return self.name + '-' + self.desc

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    desc = models.CharField(max_length=300)

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
# class Reply(models.Model):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     text = models.CharField(max_length=700)
#     #add reply button
#
# class User