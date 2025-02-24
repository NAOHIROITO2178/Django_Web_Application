from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model # ユーザーモデルを取得するため

# ユーザーモデル取得
User = get_user_model()


'''ログイン用フォーム'''
class LoginForm(AuthenticationForm):

    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


'''サインアップ用フォーム'''
class SignupForm(UserCreationForm):
    JOB_CHOICES = [
        ('', '未選択'),
        ('エンジニア', 'エンジニア'),
        ('デザイナー', 'デザイナー'),
        ('マーケター', 'マーケター'),
        ('ディレクター', 'ディレクター'),
        ('営業', '営業'),
        ('バックオフィス', 'バックオフィス'),
        ('CxO', 'CxO'),
        ('その他', 'その他'),
    ]

    job_title = forms.ChoiceField(
        choices=JOB_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    self_introduction = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '自己紹介文を入力してください（1000文字以内）'
        })
    )
    self_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'job_title', 'self_introduction', 'self_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる


'''ユーザー情報更新用フォーム'''
class UserUpdateForm(forms.ModelForm):
    JOB_CHOICES = [
        ('', '未選択'),
        ('エンジニア', 'エンジニア'),
        ('デザイナー', 'デザイナー'),
        ('マーケター', 'マーケター'),
        ('ディレクター', 'ディレクター'),
        ('営業', '営業'),
        ('バックオフィス', 'バックオフィス'),
        ('CxO', 'CxO'),
        ('その他', 'その他'),
    ]

    job_title = forms.ChoiceField(
        choices=JOB_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    self_introduction = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '自己紹介文を入力してください（1000文字以内）'
        })
    )
    self_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'job_title', 'self_introduction', 'self_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            if field.required:
                field.widget.attrs['required'] = 'required'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

'''パスワード変更フォーム'''
class MyPasswordChangeForm(PasswordChangeForm):

    # bootstrap4対応で、classを指定
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
