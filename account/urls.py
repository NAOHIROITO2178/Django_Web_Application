from django.urls import path, include
from . import views

app_name ='account'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'), # 追加
    path('logout/', views.Logout.as_view(), name='logout'), # 追加
    # ログインユーザーのマイページ
    path('my_page/', views.MyPage.as_view(), name='my_page'),  # pk不要で自分のページを表示 
    # 他のユーザーのマイページ
    path('my_page_update/', views.MyPageUpdate.as_view(), name='my_page_update'),  # pk不要で自分のページの情報を更新
    path('user_page/<int:pk>/', views.UserPage.as_view(), name='user_page'),  # 他ユーザーのページ
    path('signup/', views.Signup.as_view(), name='signup'), # サインアップ
    path('signup_done/', views.SignupDone.as_view(), name='signup_done'), # サインアップ完了
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), # パスワード変更
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'), # パスワード変更完了
    path('follow-home/<int:pk>/', views.FollowHome.as_view(), name='follow-home'),
    path('follow-detail/<int:pk>/', views.FollowDetail.as_view(),name='follow-detail'),
    path('follow-list/', views.FollowList.as_view(), name='follow-list'),
    path('delete_account/<int:pk>/', views.DeleteAccount.as_view(), name='delete_account')
]
