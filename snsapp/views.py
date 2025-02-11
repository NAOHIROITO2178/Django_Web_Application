from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django import forms
from .forms import PostForm, CommentForm  # CommentForm をインポート
import django_filters
from rest_framework import viewsets, filters
from .models import Post, Connection, Comment
from django.http import Http404
import requests, markdown
from .serializer import PostSerializer, ConnectionSerializer, CommentSerializer # TagSerializer

# pk はプライマリキーの略で、データベースの各レコードのユニークな名前です。 Post モデルでプライマリキーを指定しなかったので、
# Djangoは私たちのために1つのキーを作成し（デフォルトでは、各レコードごとに1ずつ増える数字で、たとえば1、2、3です）、
# 各投稿に pk というフィールド名で追加します。

class Home(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'snsapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MyPost(LoginRequiredMixin, ListView):
   """自分の投稿のみ表示"""
   model = Post
   template_name = 'snsapp/mypost.html'

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
    form_class = PostForm 

    def form_valid(self, form):
        form.instance.user = self.request.user
        instance = form.save()

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
    form_class = PostForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['selected_tags'] = self.object.tag.all()
        return context
    
    def form_valid(self, form):
        instance = form.save(commit=False)

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

class Search(LoginRequiredMixin, View):
    def get(self, request, *arg, **kwargs):
        post_data = Post.objects.order_by('-id')
        keyword = request.GET.get('keyword')

        if keyword:
            exclusion_list = set([' ', '  '])
            query_list = ''

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

class HowToMakdown(LoginRequiredMixin, TemplateView):
    template_name = 'snsapp/how_to_markdown.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 記述例とレンダリング結果のペア
        markdown_examples = [
            {
                "title": "見出し",
                "markdown": "# H1\n## H2\n### H3",
            },
            {
                "title": "強調",
                "markdown": "*イタリック*\n**ボールド**\n",
            },
            {
                "title": "リスト",
                "markdown": "- リストアイテム1\n- リストアイテム2\n  - ネストされたリスト",
            },
            {
                "title": "番号付きリスト",
                "markdown": "1. 番号付きリスト1\n2. 番号付きリスト2",
            },
            {
                "title": "コードブロック",
                "markdown": "```\nprint('Hello, Markdown!')\n```",
            },
            {
                "title": "リンク",
                "markdown": "[Google](https://www.google.com)",
            },
            {
                "title": "画像",
                "markdown": "![サンプル画像](https://via.placeholder.com/150)",
            },
            {
                "title": "引用",
                "markdown": "> これは引用です。\n>> ネストされた引用",
            },
            {
                "title": "表",
                "markdown": "| 見出し1 | 見出し2 |\n|--------|--------|\n| 内容1  | 内容2  |\n| 内容3  | 内容4  |",
            },
        ]

        # 各マークダウンの記述例をHTMLに変換
        for item in markdown_examples:
            item["html"] = markdown.markdown(item["markdown"], extensions=['fenced_code', 'codehilite', 'tables', 'extra'])

        context['markdown_examples'] = markdown_examples
        return context

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

    # def get_queryset(self):
    #     tag_name = self.kwargs['tag']
    #     try:
    #         tag = Tag.objects.get(name=tag_name)
    #     except Tag.DoesNotExist:
    #         raise Http404("Tag does not exist")

    #     return tag.post_set.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     tag_name = self.kwargs['tag']
    #     context['tag_name'] = tag_name
    #     return context

#ここからAPIのViewSetの定義
# class TagViewSet(viewsets.ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
