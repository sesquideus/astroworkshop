from django.contrib import admin
from django.db.models import Prefetch

from ..models import Participation, Participant


class ParticipationInline(admin.TabularInline):
    model = Participation
    fields = ('person', 'online', 'organizer')
    verbose_name = 'Účastník'
    verbose_name_plural = 'Účastníci'
    raw_id_fields = ['person']

    extra = 1

    def get_queryset(self, request):
        return super().get_queryset(request) \
                      .select_related('person', 'event') \
                      .prefetch_related(Prefetch('person', queryset=Participation.objects.select_related('event')))
