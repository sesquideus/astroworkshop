import django
from django.db.models import F, Q, ExpressionWrapper, Func, When, DateTimeField
from django.db.models.functions import TruncDay
from datetime import timedelta

from core.models import Slot


class ProgrammeView(django.views.generic.ListView):
    model = Slot
    context_object_name = 'slots'
    template_name = 'core/programme.html'

    def get_queryset(self):
        return self.model.objects \
            .with_people() \
            .filter(event__code=self.kwargs.get('year', "2021")) \
            .annotate(
                date=TruncDay('start'),
            ) \
            .order_by('start', 'duration')


class SlotView(django.views.generic.DetailView):
    model = Slot
    context_object_name = 'slot'
    template_name = 'core/slot.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_queryset(self):
        return self.model.objects.with_people().order_by('person__last_name')
