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
from accounts.views import hello_world, home, redirectToHome
from stock.views import query, showStockList, filterStock
from django.views.generic import TemplateView

# handler for 404 error and 500 error
handler404 = 'mysite.views.custom404View'
handler500 = 'mysite.views.custom500View'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('index/', home),
    path('', redirectToHome),
    path('feature/stock_list/', showStockList),
    path('feature/filter_stock/', filterStock),
    path('ranking/', include('ranking.urls'))
    # path('query/', query, name='query')
    # path('', TemplateView.as_view(template_name='main_template.html'))
]
