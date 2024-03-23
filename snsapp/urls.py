
from django.urls import path
from .views import Home, MyPost, CreatePost, DetailPost, UpdatePost, DeletePost, LikeHome, LikeDetail, FollowHome, FollowDetail, FollowList, CreateComment, UpdateComment, DeleteComment                   

urlpatterns = [
   path('', Home.as_view(), name='home'),             #追加
   path('mypost/', MyPost.as_view(), name='mypost'),  #追加 
   path('detail/<int:pk>', DetailPost.as_view(), name='detail'),
   path('create/', CreatePost.as_view(), name='create'),
   path('detail/<int:pk>/update', UpdatePost.as_view(), name='update'),
   path('detail/<int:pk>/delete', DeletePost.as_view(), name='delete'),
   path('like-home/<int:pk>', LikeHome.as_view(), name='like-home'),
   path('like-detail/<int:pk>', LikeDetail.as_view(), name='like-detail'),
   path('follow-home/<int:pk>', FollowHome.as_view(), name='follow-home'),
   path('follow-detail/<int:pk>', FollowDetail.as_view(),name='follow-detail'),
   path('follow-list/', FollowList.as_view(), name='follow-list'),
   path('comment-create/<int:pk>/', CreateComment.as_view(), name='comment-create'),
   path('comment-update/<int:pk>/', UpdateComment.as_view(), name='comment-update'),
   path('comment-delete/<int:pk>/', DeleteComment.as_view(), name='comment-delete'),
]