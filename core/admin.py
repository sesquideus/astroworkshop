import django
from django.contrib import admin
from django.db import models
from django.db.models import Prefetch
from django.forms import Textarea
from django.forms.widgets import TextInput, NumberInput
from django.utils.html import format_html_join

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group

import core
import datetime


@admin.register(core.models.Institute)
class InstituteAdmin(admin.ModelAdmin):
    pass


class AffiliationInline(admin.TabularInline):
    model = core.models.Affiliation
    extra = 1

    list_select_related = True


class ParticipationInline(admin.TabularInline):
    model = core.models.Participation
    fields = ('event', 'online', 'organizer')
    extra = 1

    list_select_related = True


class ParticipantInline(admin.TabularInline):
    model = core.models.Participation
    fields = ('person', 'online', 'organizer')
    verbose_name = 'Participant'
    verbose_name_plural = 'Participants'
    raw_id_fields = ['person']

    extra = 1


class SlotInline(admin.TabularInline):
    model = core.models.Slot
    fields = ('category', 'person', 'start', 'duration', 'title', 'abstract', 'note')
    extra = 3

    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '30'}),
        },
        models.TextField: {
            'widget': Textarea(attrs={'size': '40'}),
        },
    }

    def get_queryset(self, request):
        return self.model.objects.prefetch_related('person')


@admin.register(core.models.Participant)
class ParticipantAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = [AffiliationInline]
    ordering = ['last_name', 'first_name']
    list_display = ['get_full_name', 'list_affiliations', 'list_participations']
    form = django.contrib.auth.forms.UserChangeForm
    add_form = django.contrib.auth.forms.UserCreationForm
    readonly_fields = ['date_joined', 'last_login']

    def get_queryset(self, request):
        return core.models.Participant.objects.with_events().with_all_affiliations()

    def list_participations(self, obj):
        return ', '.join([x.code for x in obj.all_participations])
    list_participations.short_description = "zoznam účastí"

    def list_affiliations(self, obj):
        return ', '.join([x.short_name for x in obj.all_affiliations])
    list_affiliations.short_description = "zoznam afiliácií"


@admin.register(core.models.Slot)
class SlotAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    ordering = ['start']

    list_display = ['title', 'people', 'start', 'duration', 'note', 'end', 'presentation']
    list_filter = ['event', 'category']
    filter_horizontal = ['person']

    def get_queryset(self, request):
        return core.models.Slot.objects.with_people()

    def people_count(self, obj):
        return obj.people_count
    people_count.short_description = "počet autorov"

    def end(self, obj):
        if obj.start is None or obj.duration is None:
            return None
        else:
            return obj.start + datetime.timedelta(minutes=obj.duration)
    end.short_description = "koniec"

    def people(self, obj):
        return format_html_join('\n', "<li>{}</li>", [(x.__str__(),) for x in obj.people])
    people.short_description = "autori"


#@admin.register(core.models.Participation)
#class ParticipationAdmin(admin.ModelAdmin):
#    def get_queryset(self, request):
#        return self.model._default_manager.prefetch_related('person', 'event')
#

@admin.register(core.models.Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [SlotInline, ParticipantInline]

    def get_queryset(self, request):
        return self.model.objects.with_slots().with_participants()


@admin.register(core.models.Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model._default_manager.prefetch_related('person', 'institute')


admin.site.unregister(Group)
@admin.register(Group)
class NewGroupAdmin(GroupAdmin):
    list_display = ['name', 'user']
    filter_horizontal = ['permissions', 'user']
