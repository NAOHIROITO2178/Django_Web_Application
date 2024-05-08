# coding: utf-8

from rest_framework import serializers

from .models import Tag, Post, Connection, Comment

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name")

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "user", "like", "created_at", "tag")


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ("user", "following")

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content", "post", "user", "created_at")
