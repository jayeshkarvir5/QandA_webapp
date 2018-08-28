from django import forms
from .models import Question, Answer


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'topic',
            'question',
            'desc',
        ]

    def clean_question(self):
        ques = self.cleaned_data.get("question")
        if ques == 'Hello':
            raise forms.ValidationError('Not a valid question')
        return ques


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'question',
            'answer',
        ]

    def __init__(self, user=None, *args, **kwargs):
        print(user)
        super(AnswerCreateForm, self).__init__(*args, **kwargs)
        print(kwargs)
        # self.fields['question'].queryset = Question.objects.filter(slug=1)
        # self.fields['question'].queryset = Question.objects.filter(slug=sl)
        # self.fields['question'].queryset = Question.objects.filter(owner=user)
