import django
import datetime
import locale
import unicodedata

from functools import cmp_to_key

from core.models import Participant

locale.setlocale(locale.LC_ALL, "")


class ListView(django.views.generic.ListView):
    model = Participant
    context_object_name = 'participants'
    template_name = 'core/list-participants.html'

    def get_queryset(self):
        year = self.kwargs['year']
        return self.model.objects.for_event(year).with_current_affiliations(datetime.date.today()).order_by('last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = sorted(context[self.context_object_name], key=lambda x: unicodedata.normalize('NFKD', x.last_name))
        return context


class ParticipantView(django.views.generic.DetailView):
    model = Participant
    context_object_name = 'participant'
    template_name = 'core/participant.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return self.model.objects.with_talks().with_current_affiliations(datetime.date.today())
