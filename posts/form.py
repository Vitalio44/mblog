from django import forms
from posts.models import Post, UserProfile
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "slug",
            "content",
            "image",
            "keywords",
            "description",
        ]


class ContactForm(forms.Form):
    subject = forms.CharField(required=True, max_length=100)
    name = forms.CharField(required=True, max_length=100)
    sender = forms.EmailField(required=True, max_length=100)
    message = forms.CharField(required=True, max_length=1024)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']
