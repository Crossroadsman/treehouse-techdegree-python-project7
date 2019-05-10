from django.urls import re_path

from . import views

app_name = 'image_edit'
urlpatterns = [
    re_path(r'^$', views.cropper, name='cropper'),
    re_path(r'upload_image$', views.upload_image, name='upload_image'),
]
