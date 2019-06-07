from django.urls import re_path

from . import views

app_name = 'accounts'
urlpatterns = [
    # Registration-related views
    re_path(r'sign_in$', views.sign_in, name='sign_in'),
    re_path(r'sign_up$', views.sign_up, name='sign_up'),
    re_path(r'sign_out$', views.sign_out, name='sign_out'),

    # Profile-related views
    re_path(r'profile$',
            views.profile,
            name='profile'),
    re_path(r'profile/edit$',
            views.edit_profile,
            name='edit_profile'),
    re_path(r'bio$',
            views.bio,
            name='bio'),

    # Custom password-change view
    re_path(r'profile/change-password$',
            views.change_password,
            name='change_password'),
]
