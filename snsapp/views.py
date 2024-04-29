from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .forms import CommentForm  # CommentForm をインポート
from .models import Post, Connection, Comment, Tag
from django.http import Http404
# pk はプライマリキーの略で、データベースの各レコードのユニークな名前です。 Post モデルでプライマリキーを指定しなかったので、
# Djangoは私たちのために1つのキーを作成し（デフォルトでは、各レコードごとに1ずつ増える数字で、たとえば1、2、3です）、
# 各投稿に pk というフィールド名で追加します。

class Home(LoginRequiredMixin, ListView):
   """HOMEページで、すべてのユーザー投稿をリスト表示"""
   model = Post
   template_name = 'list.html'

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

    def form_valid(self, form):
        form.instance.user = self.request.user
        instance = form.save()

        # ハッシュタグの追加
        tags_input = self.request.POST.get('tags', '')  # フォームからハッシュタグの文字列を取得
        tags_list = tags_input.split()  # スペースで区切ってリストに変換
        for tag_name in tags_list:
            if tag_name.startswith('#'):  # ハッシュタグの場合
                tag_name = tag_name[1:]  # ハッシュタグ記号を削除
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tag.add(tag)

        return super().form_valid(form)

    success_url = reverse_lazy('mypost')

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'update.html'
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_tags'] = self.object.tag.all()
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)

        # 既存のタグをクリアして、新しいタグを追加する
        instance.tag.clear()

         # 既存のタグの処理
        tags_input = self.request.POST.get('tags', '')  # 入力フィールドから既存のタグを取得
        tags_list = tags_input.split()  # スペースで区切ってリストに変換
        for tag_name in tags_list:
            tag_name = tag_name.strip('#')  # ハッシュタグ記号を削除
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tag.add(tag)

        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.pk})  # リダイレクト先のURLを指定します

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
        words = form.cleaned_data["text"].split()
        for word in words:
            if word[0] == "#":
                if Tag.objects.filter(name=word[1:]).exists():
                    tag = Tag.objects.get(name=word[1:])
                else:
                    tag = Tag.objects.create(name=word[1:])
                post.tag.add(tag)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'update_comment.html'

    def get_success_url(self):
        words = form.cleaned_data["text"].split()
        for word in words:
            if word[0] == "#":
                if Tag.objects.filter(name=word[1:]).exists():
                    tag = Tag.objects.get(name=word[1:])
                else:
                    tag = Tag.objects.create(name=word[1:])
                post.tag.add(tag)
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
      #投稿の特定
      pk = self.kwargs['pk']
      super().get(request, *args, **kwargs)
      return redirect('home')

class LikeDetail(LikeBase):
  def get(self, request, *args, **kwargs):
      #投稿の特定
      pk = self.kwargs['pk']
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

class TaggedPosts(ListView):
    model = Post
    template_name = 'tagged_posts.html'

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            raise Http404("Tag does not exist")

        return tag.post_set.all()
