from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput, NumberInput

import core
import datetime

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


@admin.register(core.models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline, ParticipationInline]

    list_display = ['get_full_name', 'list_affiliations']

    def list_affiliations(self, obj):
        return ', '.join([x.short_name for x in obj.affiliations.all()])
    list_affiliations.short_description = "List of affiliations"


@admin.register(core.models.Slot)
class SlotAdmin(admin.ModelAdmin):
    ordering = ['start']

    list_display = ['title', 'people', 'start', 'duration', 'end']
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
        return ', '.join([x.__str__() for x in obj.people])
    people.short_description = "Authors"


class SlotInline(admin.TabularInline):
    model = core.models.Slot
    fields = ('start', 'duration', 'title', 'abstract', 'person', 'category')
    extra = 3

    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '100'}),
        },
    }


@admin.register(core.models.Participation)
class ParticipationAdmin(admin.ModelAdmin):
    pass

@admin.register(core.models.Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [SlotInline]

@admin.register(core.models.Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass
