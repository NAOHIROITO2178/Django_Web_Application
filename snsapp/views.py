from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .forms import CommentForm  # CommentForm をインポート
from .models import Post, Connection, Comment

# pk はプライマリキーの略で、データベースの各レコードのユニークな名前です。 Post モデルでプライマリキーを指定しなかったので、
# Djangoは私たちのために1つのキーを作成し（デフォルトでは、各レコードごとに1ずつ増える数字で、たとえば1、2、3です）、
# 各投稿に pk というフィールド名で追加します。

class Home(LoginRequiredMixin, ListView):
   """HOMEページで、自分以外のユーザー投稿をリスト表示"""
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
       #リクエストユーザーのみ除外
       return Post.objects.exclude(user=self.request.user)

class MyPost(LoginRequiredMixin, ListView):
   """自分の投稿のみ表示"""
   model = Post
   template_name = 'list.html'

   def get_queryset(self):
     #自分の投稿に限定
       return Post.objects.filter(user=self.request.user)

class DetailPost(LoginRequiredMixin, DetailView):
   """投稿詳細ページ"""
   model = Post
   template_name = 'detail.html'

class CreatePost(LoginRequiredMixin, CreateView):
  model = Post
  template_name = 'create.html'
  fields = ['title', 'content']
  success_url = reverse_lazy('mypost')
  
  def form_valid(self, form):
    """投稿ユーザーをリクエストユーザーと紐付け"""
    form.instance.user = self.request.user
    return super().form_valid(form)

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  template_name = 'update.html'
  fields = ['title', 'content']

  def get_success_url(self, **kwargs):
      """編集完了後の遷移先"""
      pk = self.kwargs["pk"]
      return reverse_lazy('detail', kwargs={"pk": pk})
    
  def test_func(self, **kwargs):
      """アクセスできるユーザーを制限"""
      pk = self.kwargs["pk"]
      post = Post.objects.get(pk=pk)
      return (post.user == self.request.user)

class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'delete.html'
  success_url = reverse_lazy('mypost')

  def test_func(self, **kwargs):
    pk = self.kwargs["pk"]
    post = Post.objects.get(pk=pk)
    return (post.user == self.request.user)

class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'create_comment.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user


class LikeBase(LoginRequiredMixin, View):
   """いいねのベース。リダイレクト先を以降で継承先で設定"""
   def get(self, request, *args, **kwargs):
    pk = self.kwargs['pk']
    related_post = Post.objects.get(pk=pk)

    if self.request.user in related_post.like.all():
       obj = related_post.like.remove(self.request.user)
    else:
       obj = related_post.like.add(self.request.user)
    return obj

class LikeHome(LikeBase):
  """HOMEページでいいねした場合"""
  def get(self, request, *args, **kwargs):
      super().get(request, *args, **kwargs)
      return redirect('home')

class LikeDetail(LikeBase):
  def get(self, request, *args, **kwargs):
      super().get(request, *args, **kwargs)
      return redirect('detail', pk)

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
   template_name = 'list.html'

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
