"""project_7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path, include
import django.contrib.auth.views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls', namespace='accounts')),
    re_path(r'^avatar/', include('image_editor.urls', namespace='image_editor')),
    #re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^$', views.home, name='home'),

    # Django's built-in password-reset views
    # Django expects the related templates to be in `/registration/`
    re_path(r'account/password-reset$',
            auth_views.PasswordResetView.as_view(),
            name="password_reset"),  # `password_reset_form.html`
    re_path(r'account/password-reset/done$',
            auth_views.PasswordResetDoneView.as_view(),
            name="password_reset_done"),  # `password_reset_done.html`
    re_path(r'account/password-reset/confirm/(?P<uidb64>[\w+]+)/(?P<token>[-\w]+)$',
            auth_views.PasswordResetConfirmView.as_view(),
            name="password_reset_confirm"),  # `password_reset_confirm.html`
    re_path(r'account/password-reset/complete$',
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete"),  # `password_reset_complete.html`

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
