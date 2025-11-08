from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from ..models import User
from .base import BaseModelAdmin

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin[User], BaseModelAdmin):  # type: ignore[misc]
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, BaseModelAdmin):  # type: ignore[misc]
    pass
