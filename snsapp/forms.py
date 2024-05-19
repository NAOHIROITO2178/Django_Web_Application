from django import forms  
from .models import Comment  # Comment モデルをインポート

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class SearchForm(forms.Form):
    query = forms.CharField(label='検索')
