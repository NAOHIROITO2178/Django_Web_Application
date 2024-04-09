from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
   title = models.CharField(max_length=100)
   content = MarkdownxField('本文', help_text='Markdown形式で書いてください。')
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   like = models.ManyToManyField(User, related_name='related_post', blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   tag = models.ManyToManyField(Tag)

   def __str__(self):
       return self.title

   class Meta:
       ordering = ["-created_at"] 

class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    content = MarkdownxField('本文', help_text='Markdown形式で書いてください。')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

