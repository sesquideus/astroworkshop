import datetime

from django.db import models
from django.contrib import admin
from django.utils.html import format_html_join
from django.forms import Textarea
from django.forms.widgets import TextInput, NumberInput

from ..models import Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    ordering = ['start']

    list_display = ['title', 'category', 'people', 'start', 'duration', 'note', 'end', 'presentation']
    list_filter = ['event', 'category']
    filter_horizontal = ['person']

    def get_queryset(self, request):
        return Slot.objects.with_people()

    @admin.display(description="počet autorov")
    def people_count(self, obj):
        return obj.people_count

    @admin.display(description="koniec")
    def end(self, obj):
        if obj.start is None or obj.duration is None:
            return None
        else:
            return obj.start + datetime.timedelta(minutes=obj.duration)

    @admin.display(description="autori")
    def people(self, obj):
        return format_html_join('\n', "<li>{}</li>", [(x.__str__(),) for x in obj.people])


class SlotInline(admin.TabularInline):
    model = Slot
    fields = ('category', 'person', 'start', 'duration', 'title', 'abstract', 'note')
    extra = 3
    autocomplete_fields = ['person']

    formfield_overrides = {
        models.CharField: {
            'widget': TextInput(attrs={'size': '30'}),
        },
        models.TextField: {
            'widget': Textarea(attrs={'size': '40'}),
        },
    }

    def get_queryset(self, request):
        return self.model.objects.prefetch_related('person__affiliation__institute', 'person__participations__event')
