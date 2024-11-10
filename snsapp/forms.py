from django import forms  
from .models import Post, Comment  # Comment モデルをインポート

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tag'] 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
