from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
   # path('admin/', admin.site.urls),
   path('accounts/', include('allauth.urls')), 
   path('', include('snsapp.urls')), 
]

# itounaohiro@itounaohironoMacBook-Pro snsproject % python3 manage.py createsuperuser
# ユーザー名 (leave blank to use 'itounaohiro'): NI_Python
# メールアドレス: Django@example.com
# Password: Python1278
# Password (again): Python1278
# Superuser created successfully.