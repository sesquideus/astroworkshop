import datetime
import django
import pytz
from django.db.models import F, Q, ExpressionWrapper, Func, When, DateTimeField
from django.db.models.functions import TruncDay

import core
from core.models import Event


class ProgrammeView(django.views.generic.ListView):
    model = core.models.Slot
    context_object_name = 'slots'
    template_name = 'core/programme.html'

    def get_queryset(self):
        self.event = django.shortcuts.get_object_or_404(core.models.Event,
                                                        code=self.kwargs.get('year', datetime.date.today().year))

        qs = self.model.objects \
            .with_people() \
            .filter(event__code=self.event.code) \
            .annotate(
                date=TruncDay('start'),
            ) \
            .order_by('start', 'duration')
        return qs

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) \
            | {'current_event': self.event} \
            | {'events': Event.objects.for_user(self.request.user).order_by('-code')}


class DayProgrammeView(ProgrammeView):
    template_name = 'core/programme-abstract.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            date=datetime.datetime(self.kwargs['year'], self.kwargs['month'], self.kwargs['day'],
                                   0, 0, 0, tzinfo=pytz.utc)
        )


class SlotView(django.views.generic.DetailView):
    model = core.models.Slot
    context_object_name = 'slot'
    template_name = 'core/slot.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_queryset(self):
        return self.model.objects.with_people()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
