from django.contrib import admin

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group


admin.site.unregister(Group)


@admin.register(Group)
class NewGroupAdmin(GroupAdmin):
    list_display = ['name']
