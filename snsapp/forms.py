from django import forms
from markdownx.fields import MarkdownxFormField
from .models import Comment, Post  # Comment モデルをインポート

class PostForm(forms.ModelForm):
    content = MarkdownxFormField()  # MarkdownxFormField を使用して content フィールドを作成

    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
