from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ParticipantAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('is_active',)


admin.site.unregister(User)
admin.site.register(User, ParticipantAdmin)
