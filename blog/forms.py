from django import forms
from .models import Comment, Post


class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']