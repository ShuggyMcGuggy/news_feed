""" Defines the URL patterns for users"""

from django.conf.urls import url
from django.contrib.auth.views import auth_login
# from django.contrib.auth import authenticate, login, urls
from django.contrib.auth import views as auth_views

from . import views
app_name = 'users'

urlpatterns = [
    # Login Page
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    # url(r'^login/$', auth_login(),  name='login'),

    # Logout Page
    url(r'^logout/$', views.logout_view, name='logout'),

    # # Registration page
    # url(r'^register/$', views.register, name='register'),
    ]