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

    class Meta:
        model = User
        fields = ('email','username')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = '' # 全フィールドを入力必須

            # オートフォーカスとプレースホルダーの設定
            print(field.label)
            if field.label == 'メールアドレス':
                field.widget.attrs['placeholder'] = '***@gmail.com'

'''ユーザー情報更新用フォーム'''
class UserUpdateForm(forms.ModelForm):
    job_title = forms.ChoiceField(
        choices=[
            ('Non_selected', ''),
            ('Engineer', 'エンジニア'),
            ('Designer', 'デザイナー'),
            ('Marketer', 'マーケター'),
            ('Director', 'ディレクター'),
            ('Sales', '営業'),
            ('CxO', 'CxO'),
            ('Other', 'その他')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': '自己紹介文を入力してください（1000文字以内）'
            }),
        required=False
    )

    class Meta:
        model = User
        fields = ('email', 'username',)

    # bootstrap4対応
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = '' # 全フィールドを入力必須

'''パスワード変更フォーム'''
class MyPasswordChangeForm(PasswordChangeForm):

    # bootstrap4対応で、classを指定
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
