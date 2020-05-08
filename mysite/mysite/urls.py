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
from django.urls import path, include, re_path
from accounts.views import hello_world, home, redirect_to_home, login, logout, signup, activate
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('accounts/login/', login, name='login'),
    path('accounts/logout/', logout, name='logout'),
    path('accounts/signup/', signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name="activate"),
    path('index/', home),
    path('', redirect_to_home),
    # path('', TemplateView.as_view(template_name='main_template.html'))
]
