from django import forms
from .models import Comment, Post

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']


class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']