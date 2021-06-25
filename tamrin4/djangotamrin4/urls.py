"""djangotamrin4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from user.views import CreateUser, Search, NewSearch, EditNumber, PhoneListAPI, ActionView, PhoneBook
from django.views.generic.base import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('numbers', PhoneListAPI)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', CreateUser.as_view(), name='create'),
    path('search/', Search.as_view(), name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('newsearch/', NewSearch.as_view(), name='new search'),
    path('phonebook/', cache_page(60 * 15)(PhoneBook.as_view()), name='phonebook'),
    path('editnumber/<int:pk>', EditNumber.as_view(), name='edit'),
    path('phone/api/v1/', include(router.urls)),
    path('action/', ActionView.as_view(), name='action'),
    path('__debug__/', include(debug_toolbar.urls)),
]
