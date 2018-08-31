from django.urls import re_path

from . import views

app_name = 'accounts'
urlpatterns = [
    # Registration-related views
    re_path(r'sign_in/$', views.sign_in, name='sign_in'),
    re_path(r'sign_up/$', views.sign_up, name='sign_up'),
    re_path(r'sign_out/$', views.sign_out, name='sign_out'),

    # Profile-related views
    re_path(r'(?P<user_id>\d+)/profile$',
            views.profile,
            name='profile'),
    re_path(r'(?P<user_id>\d+)/profile/edit',
            views.edit_profile,
            name='edit_profile'),
    re_path(r'(?P<user_id>\d+)/bio',
            views.bio,
            name='bio'),
]