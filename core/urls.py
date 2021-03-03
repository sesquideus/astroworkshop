from django.urls import path, re_path
from django.contrib.auth import views as authViews

from .views import slot, participant

urlpatterns = [
    path('', slot.ProgrammeView.as_view(), name='default'),
    path('<int:year>/', slot.ProgrammeView.as_view(), name='programme'),
    path('<int:year>/<int:month>/<int:day>/', slot.DayProgrammeView.as_view(), name='programme-day'),
    path('<int:year>/participants', participant.ListView.as_view(), name='participants'),
    path('talk/<int:id>/', slot.SlotView.as_view(), name='slot'),

    path('people/<slug:username>/', participant.ParticipantView.as_view(), name='participant'),
    path('login', authViews.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout', authViews.LogoutView.as_view(template_name='core/logout.html', next_page='default'), name='logout'),
]

