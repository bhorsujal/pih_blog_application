from django import forms
from .models import Comment

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']