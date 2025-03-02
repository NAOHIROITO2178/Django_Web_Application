# coding: utf-8

from rest_framework import serializers

from .models import Tag, Post, Connection, Comment

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__' 


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields ='__all__' 


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__' 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__' 
