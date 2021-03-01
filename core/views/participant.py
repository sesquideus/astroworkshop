import django
from datetime import timedelta

from core.models import Participant


class ListView(django.views.generic.ListView):
    model = Participant
    context_object_name = 'participants'
    template_name = 'core/list-participants.html'

    def get_queryset(self):
        return self.model.objects.filter(participations__code=self.kwargs['year']).order_by('last_name')


class ParticipantView(django.views.generic.DetailView):
    model = Participant
    context_object_name = 'participant'
    template_name = 'core/participant.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
