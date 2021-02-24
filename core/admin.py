from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput, NumberInput

import core

# Register your models here.

@admin.register(core.models.Institute)
class InstitudeAdmin(admin.ModelAdmin):
    pass


class AffiliationInline(admin.TabularInline):
    model = core.models.Affiliation


@admin.register(core.models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    inlines = [AffiliationInline]


@admin.register(core.models.Slot)
class SlotAdmin(admin.ModelAdmin):
    ordering = ['start']

    list_display = ['title', 'start']
    list_filter = ['event']

    def get_queryset(self, request):
        return core.models.Slot.objects.with_people()


class SlotInline(admin.TabularInline):
    model = core.models.Slot
    fields = ('start', 'duration', 'title', 'abstract', 'category')

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
