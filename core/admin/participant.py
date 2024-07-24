from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from ..models import Participant, Participation
from .affiliation import AffiliationInline


@admin.register(Participant)
class ParticipantAdmin(UserAdmin):
    inlines = [AffiliationInline]
    ordering = ['last_name', 'first_name']
    list_filter = UserAdmin.list_filter + ('is_active',)
    list_display = ['get_full_name', 'list_affiliations', 'list_participations']
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ['date_joined', 'last_login']

    def get_queryset(self, request):
        return Participant.objects.with_events().with_all_affiliations()

    @admin.display(description="zoznam účastí")
    def list_participations(self, obj):
        return ', '.join([x.code for x in obj.all_participations])

    @admin.display(description="zoznam afiliácií")
    def list_affiliations(self, obj):
        return ', '.join([x.institute.short_name for x in obj.all_affiliations])
