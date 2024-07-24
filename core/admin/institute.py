from django.contrib import admin

from ..models import Institute


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'full_name']
    ordering = ['short_name', 'full_name']
