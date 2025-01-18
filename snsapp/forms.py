from django import forms  
from .models import Post, Comment  # Comment モデルをインポート

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category'] 

        category = forms.ChoiceField(
            choices=Post.CATEGORY_CHOICES,  # モデルのCATEGORY_CHOICESを使用
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='カテゴリ'
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
