from django.urls import re_path

from . import views

app_name = 'accounts'
urlpatterns = [
    re_path(r'sign_in/$', views.sign_in, name='sign_in'),
    re_path(r'sign_up/$', views.sign_up, name='sign_up'),
    re_path(r'sign_out/$', views.sign_out, name='sign_out'),
]