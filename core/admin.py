from django.contrib import admin
from django.db import models
from django.db.models import Prefetch
from django.forms import Textarea
from django.forms.widgets import TextInput, NumberInput
from django.utils.html import format_html, format_html_join

import core
import datetime

from core.models import Participant

# Register your models here.

@admin.register(core.models.Institute)
class InstitudeAdmin(admin.ModelAdmin):
    pass


class AffiliationInline(admin.TabularInline):
    model = core.models.Affiliation
    extra = 1


class ParticipationInline(admin.TabularInline):
    model = core.models.Participation
    fields = ('event', 'online', 'organizer')
    extra = 1


class ParticipantInline(admin.TabularInline):
    model = core.models.Participation
    fields = ('person', 'online', 'organizer')
    extra = 1


class SlotInline(admin.TabularInline):
    model = core.models.Slot
    fields = ('person', 'start', 'duration', 'title', 'abstract', 'note', 'category')
    extra = 3
 
    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '30'}),
        },
        models.TextField: {
            'widget': Textarea(attrs={'size': '40'}),
        },
    }


@admin.register(core.models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline, ParticipationInline]

    list_display = ['get_full_name', 'list_affiliations', 'list_participations']

    def get_queryset(self, request):
        return core.models.Participant.objects.with_events().with_all_affiliations()

    def list_participations(self, obj):
        return ', '.join([x.code for x in obj.all_participations])
    list_participations.short_description = "List of participations"

    def list_affiliations(self, obj):
        return ', '.join([x.short_name for x in obj.all_affiliations])
    list_affiliations.short_description = "List of affiliations"


@admin.register(core.models.Slot)
class SlotAdmin(admin.ModelAdmin):
    ordering = ['start']

    list_display = ['title', 'people', 'start', 'duration', 'note', 'end', 'presentation']
    list_filter = ['event']

    def get_queryset(self, request):
        return core.models.Slot.objects.with_people()

    def people_count(self, obj):
        return obj.people_count
    people_count.short_description = "Author count"

    def end(self, obj):
        if obj.start is None or obj.duration is None:
            return None
        else:
            return obj.start + datetime.timedelta(minutes=obj.duration)

    end.short_description = "End"

    def people(self, obj):
        return format_html_join('\n', "<li>{}</li>", [(x.__str__(),) for x in obj.people])
    people.short_description = "Authors"


@admin.register(core.models.Participation)
class ParticipationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model._default_manager.prefetch_related('person', 'event')


@admin.register(core.models.Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [SlotInline, ParticipantInline]

#    def get_queryset(self, request):
#        return core.models.Event.objects.prefetch_related('slots__person')


@admin.register(core.models.Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model._default_manager.prefetch_related('person', 'institute')
