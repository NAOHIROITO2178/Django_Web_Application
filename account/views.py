from django.shortcuts import render, redirect, resolve_url # 追加
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView # 追加
from django.contrib.auth import get_user_model # 追加
from django.contrib.auth.mixins import UserPassesTestMixin # 追加
from .forms import LoginForm, SignupForm, UserUpdateForm, MyPasswordChangeForm # 追加
from django.urls import reverse_lazy # 追加　遅延評価用
from django.contrib.auth import get_user_model # 追加
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from snsapp.models import Post, Connection

# Create your views here.

User = get_user_model()

class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('snsapp:home')

'''追加'''
class Logout(LogoutView):
    template_name = 'account/logout_done.html'

    def get_success_url(self):
        return reverse_lazy('account:logout')

'''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


'''マイページ'''
class MyPage(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'account/my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される

'''サインアップ'''
class Signup(generic.CreateView):
    template_name = 'account/user_form.html'
    form_class =SignupForm

    def form_valid(self, form):
        user = form.save() # formの情報を保存
        return redirect('account:signup_done')

    # データ送信
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Sign up"
        return context


'''サインアップ完了'''
class SignupDone(generic.TemplateView):
    template_name = 'account/signup_done.html'

'''ユーザー登録情報の更新'''
class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'account/user_form.html'

    def get_success_url(self):
        return resolve_url('account:my_page', pk=self.kwargs['pk'])

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Update"
        return context

    def get_initial(self):
        # 初期値としてサインアップ時の値をフォームに表示
        initial = super().get_initial()
        user = self.get_object()
        return initial

'''パスワード変更'''
class PasswordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/user_form.html'

    # contextデータ作成
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Change Password"
        return context

'''パスワード変更完了'''
class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'

class DeleteAccount(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "account/delete_account_confirm.html"
    success_url = reverse_lazy('account:login')

    def get_object(self, queryset=None):
        return self.request.user

class FollowBase(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    # ユーザの特定
    pk = self.kwargs['pk']
    target_user = Post.objects.get(pk=pk).user
    #ユーザー情報よりコネクション情報を取得。存在しなければ作成
    my_connection = Connection.objects.get_or_create(user=self.request.user)
    #フォローテーブル内にすでにユーザーが存在する場合
    if target_user in my_connection[0].following.all():
       #テーブルからユーザーを削除
       obj = my_connection[0].following.remove(target_user)
    else:
       #テーブルにユーザーを追加
       obj = my_connection[0].following.add(target_user)
    return obj

class FollowHome(FollowBase):
  def get(self, request, *args, **kwargs):
    #FollowBaseでリターンしたobj情報を継承
    super().get(request, *args, **kwargs)
    #homeにリダイレクト
    return redirect('home')
      
class FollowDetail(FollowBase):
  def get(self, request, *args, **kwargs):
     #FollowBaseでリターンしたobj情報を継承
    super().get(request, *args, **kwargs)
    pk = self.kwargs['pk']
    #detailにリダイレクト
    return redirect('detail', pk)

class FollowList(LoginRequiredMixin, ListView):
   """フォローしたユーザーの投稿をリスト表示"""
   model = Post
   template_name = 'snsapp/follow_list.html'

   def get_queryset(self):
      """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
      my_connection = Connection.objects.get_or_create(user=self.request.user)
      all_follow = my_connection[0].following.all()
      #投稿ユーザーがフォローしているユーザーに含まれている場合オブジェクトを返す。
      return Post.objects.filter(user__in=all_follow)

   def get_context_data(self, *args, **kwargs):
       """コネクションに関するオブジェクト情報をコンテクストに追加"""
       context = super().get_context_data(*args, **kwargs)
       context['connection'] = Connection.objects.get_or_create(user=self.request.user)
       return context