from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django import forms
from .forms import CommentForm  # CommentForm をインポート
import django_filters
from rest_framework import viewsets, filters
from .models import Post, Connection, Comment, Tag
from django.http import Http404
import requests
from .serializer import PostSerializer, ConnectionSerializer, CommentSerializer, TagSerializer
# pk はプライマリキーの略で、データベースの各レコードのユニークな名前です。 Post モデルでプライマリキーを指定しなかったので、
# Djangoは私たちのために1つのキーを作成し（デフォルトでは、各レコードごとに1ずつ増える数字で、たとえば1、2、3です）、
# 各投稿に pk というフィールド名で追加します。

def fetch_news():
    # NewsAPIから日本語のIT・Web業界関連の新しいニュースを取得
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "jp",
        "category": "technology",
        "apiKey": "036575c5614545aba8aa0cb6d40e3b1d"  # ここに自分のAPIキーを入力
    }
    response = requests.get(url, params=params)
    data = response.json()
    articles = data.get("articles", [])
    return articles[:4]

class Home(LoginRequiredMixin, ListView):
    """HOMEページで、日本語のIT・Web業界関連の新着ニュースを表示"""
    model = Post
    template_name = 'snsapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # NewsAPIからニュースを取得
        news = fetch_news()
        context['news'] = news
        return context

class MyPost(LoginRequiredMixin, ListView):
   """自分の投稿のみ表示"""
   model = Post
   template_name = 'snsapp/list.html'

   def get_queryset(self):
     #自分の投稿に限定
       return Post.objects.filter(user=self.request.user)

class DetailPost(LoginRequiredMixin, DetailView):
   """投稿詳細ページ"""
   model = Post
   template_name = 'snsapp/detail.html'

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'snsapp/create.html'
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

    def get_success_url(self):
        return reverse_lazy('snsapp:confirm_create', kwargs={'pk': self.object.pk})

class ConfirmCreatePost(LoginRequiredMixin, TemplateView):
    template_name = 'snsapp/confirm_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

    success_url = reverse_lazy('snsapp:mypost')

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'snsapp/update.html'
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
        return reverse_lazy('snsapp:confirm_update', kwargs={'pk': self.object.pk})

class ConfirmUpdatePost(LoginRequiredMixin, TemplateView):
    template_name = 'snsapp/confirm_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

    success_url = reverse_lazy('snsapp:mypost')

class ConfirmDeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'snsapp/confirm_delete.html'
    success_url = reverse_lazy('snsapp:mypost')

    def test_func(self, **kwargs):
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return post.user == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        if "confirm" in request.POST:
            return self.delete(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class CreateComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'snsapp/create_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])  # Postオブジェクトを取得してコンテキストに追加
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        text = form.cleaned_data.get("text", "")  # "text"キーが存在するかチェックして取得
        words = text.split()        
        for word in words:
            if word.startswith("#"):  # 文字列の先頭が "#" かどうかを確認
                tag_name = word[1:]  # "#" を取り除いたタグ名
                tag, created = Tag.objects.get_or_create(name=tag_name)  # 存在しない場合は新規作成
                form.instance.post.tag.add(tag)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('snsapp:confirm_create_comment', kwargs={'pk': self.object.pk})

class ConfirmCreateComment(LoginRequiredMixin, TemplateView):
    template_name = 'snsapp/confirm_create_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        context['post'] = comment.post  # コメントに関連するPostを取得
        context['comment'] = comment
        return context

    def get_success_url(self):
        # pkが正しく渡されているか確認
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return reverse_lazy('detail', kwargs={'pk': comment.post.pk})

class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'snsapp/update_comment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()  # 現在のコメントオブジェクトを取得
        context['post'] = comment.post  # コメントに関連するPostを取得
        return context

    def get_success_url(self):
        comment = self.get_object()  # 現在のコメントオブジェクトを取得
        text = comment.content  # コメントのテキストを取得
        words = text.split()
        for word in words:
            if word.startswith("#"):
                tag_name = word[1:]
                tag, created = Tag.objects.get_or_create(name=tag_name)
                comment.post.tag.add(tag)  # コメントが属する投稿のタグに追加
        return reverse_lazy('snsapp:confirm_update_comment', kwargs={'pk': comment.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

class ConfirmUpdateComment(LoginRequiredMixin, TemplateView):
    template_name = 'snsapp/confirm_update_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        context['post'] = comment.post  # コメントに関連するPostを取得
        context['comment'] = comment
        return context

    def get_success_url(self):
        # pkが正しく渡されているか確認
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return reverse_lazy('detail', kwargs={'pk': comment.post.pk})

class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'snsapp/delete_comment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.get_object()
        context['post'] = comment.post  # コメントに関連するPostを取得
        context['comment'] = comment
        return context

    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('detail', kwargs={'pk': comment.post.pk})

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

class TaggedPosts(ListView):
    model = Post
    template_name = 'snsapp/tagged_posts.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        try:
            tag = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            raise Http404("Tag does not exist")

        return tag.post_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs['tag']
        context['tag_name'] = tag_name
        return context

#ここからAPIのViewSetの定義
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
