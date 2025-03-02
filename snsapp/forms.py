from django import forms  
from .models import Tag, Post, Comment
from django.core.exceptions import ValidationError
import re

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'カンマ区切りでタグを入力してください'}),
        label='タグ'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags'] 

    category = forms.ChoiceField(
        choices=Post.CATEGORY_CHOICES,  # モデルのCATEGORY_CHOICESを使用
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='カテゴリ'
    )


    def clean_tags(self):
        tags_str = self.cleaned_data.get('tags', '')
        tag_names = [name.strip() for name in tags_str.split(',')]
        for name in tag_names:
            if not re.match(r'^[\w\s-]+$', name):
                raise ValidationError(f"タグ名 '{name}' に無効な文字が含まれています。")
        return tags_str

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
