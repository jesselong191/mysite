"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from login import views

urlpatterns = [
# path()方法可以接受4个参数，其中2个是必须的：route 和 view  2个可选参数：kwargs （关键字参数）和name（URL 命名）
    path('admin/', admin.site.urls),
    path('polls/',include('polls.urls')),
    path('index/',views.index),
    path('register/',views.register),
    path('login/',views.login),
    path('logout/',views.logout),
    path('captcha',include('captcha.urls')),#图片验证
    path('confirm/',views.user_confirm),
]
