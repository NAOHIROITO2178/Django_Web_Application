from django.urls import path
from .views import TagViewSet, PostViewSet, ConnectionViewSet, CommentViewSet, Home, MyPost, DetailPost, CreatePost, ConfirmCreatePost, UpdatePost, ConfirmUpdatePost, ConfirmDeletePost, LikeHome, LikeDetail, CreateComment, UpdateComment, DeleteComment, HowToMakdown, TaggedPosts, ConfirmCreateComment, ConfirmUpdateComment
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('connections', ConnectionViewSet)
router.register('comments', CommentViewSet)
router.register('tags', TagViewSet)

urlpatterns = router.urls

app_name ='snsapp'

urlpatterns += [
   path('home/', Home.as_view(), name='home'),      
   path('mypost/', MyPost.as_view(), name='mypost'),   
   path('detail/<int:pk>/', DetailPost.as_view(), name='detail'),
   path('create/', CreatePost.as_view(), name='create'),
   path('create/confirm/<int:pk>/', ConfirmCreatePost.as_view(), name='confirm_create'),
   path('detail/<int:pk>/update/', UpdatePost.as_view(), name='update'),
   path('detail/<int:pk>/update_confirm/', ConfirmUpdatePost.as_view(), name='confirm_update'),
   path('detail/<int:pk>/delete_confirm/', ConfirmDeletePost.as_view(), name='confirm_delete'),
   path('like-home/<int:pk>/', LikeHome.as_view(), name='like-home'),
   path('like-detail/<int:pk>/', LikeDetail.as_view(), name='like-detail'),
   path('comment-create/<int:pk>/', CreateComment.as_view(), name='comment-create'),
   path('comment-create_confirm/<int:pk>/', ConfirmCreateComment.as_view(), name='confirm_create_comment'),
   path('comment-update/<int:pk>/', UpdateComment.as_view(), name='comment-update'),
   path('comment-update_confirm/<int:pk>/', ConfirmUpdateComment.as_view(), name='confirm_update_comment'),
   path('comment-delete/<int:pk>/', DeleteComment.as_view(), name='comment-delete'),
   path('how_to_markown/', HowToMakdown.as_view(), name='how_to_markown'),
   path('tag/<str:tag>/', TaggedPosts.as_view(), name='tagged-posts'),
]
