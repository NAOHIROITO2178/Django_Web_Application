from django.urls import path, include
from . import views

app_name ='account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'), # 追加
    path('logout/', views.Logout.as_view(), name='logout'), # 追加
    path('my_page/<int:pk>/', views.MyPage.as_view(), name='my_page'), # 追加
    path('user_update/<int:pk>', views.UserUpdate.as_view(), name='user_update'), # 登録情報の更新
    path('signup/', views.Signup.as_view(), name='signup'), # サインアップ
    path('signup_done/', views.SignupDone.as_view(), name='signup_done'), # サインアップ完了
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), # パスワード変更
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'), # パスワード変更完了
    path('follow-home/<int:pk>/', FollowHome.as_view(), name='follow-home'),
    path('follow-detail/<int:pk>/', FollowDetail.as_view(),name='follow-detail'),
    path('follow-list/', FollowList.as_view(), name='follow-list'),
]
