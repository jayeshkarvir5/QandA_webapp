from django import forms
from .models import Question, Answer, Profile
from django.contrib.auth import get_user_model


User = get_user_model()


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
            'answer',
        ]

    def __init__(self, user=None, *args, **kwargs):
        super(AnswerCreateForm, self).__init__(*args, **kwargs)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'desc',
            'pic'
        ]

    def __init__(self, user=None, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Cannot use this email.It's already registered.")
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        # user.is_active = False
        # create a new user hash for activating email.

        if commit:
            user.save()
        return user
