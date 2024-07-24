from django.contrib import admin

from ..models import Event
from .slot import SlotInline
from .participation import ParticipationInline


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [ParticipationInline]
    list_display = ['name', 'code', 'start', 'end', 'visible']

    def get_queryset(self, request):
        return self.model.objects.with_slots().with_participants()
