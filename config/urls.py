from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
   path('admin/', admin.site.urls),
   path('accounts/', include('allauth.urls')), 
   path('', include('snsapp.urls')), 
]

# itounaohiro@itounaohironoMacBook-Pro snsproject % python3 manage.py createsuperuser
# ユーザー名 (leave blank to use 'itounaohiro'): NI_Django
# メールアドレス: Python3@example.com
# Password: Python378
# Password (again): Python378
# Superuser created successfully.

# ユーザー名 (leave blank to use 'itounaohiro'): NI_Rails
# メールアドレス: ruby@example.com
# Password: Ruby278278
# Password (again): Ruby278278
# Superuser created successfully.

# ユーザー名 (leave blank to use 'itounaohiro'): NI_Laravel
# メールアドレス: php@example.com
# Password: PHP178178
# Password (again): PHP178178
# Superuser created successfully.
