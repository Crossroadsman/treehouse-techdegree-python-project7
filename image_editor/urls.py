from django.urls import re_path

from . import views

app_name = 'image_editor'
urlpatterns = [
    re_path(r'avatar/$', views.edit_avatar, name='edit_avatar'),
]