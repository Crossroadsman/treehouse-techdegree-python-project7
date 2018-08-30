from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import P7User
from .forms import P7UserCreationForm, P7UserChangeForm


class P7UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = P7UserChangeForm
    add_form = P7UserCreationForm

    # The fields to be used in displaying the User model. These override the
    # definitions in the base UserAdmin that reference specific fields on
    # auth.User
    list_display = ('email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(P7User, P7UserAdmin)
