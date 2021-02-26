from django.urls import path, re_path
from django.contrib.auth import views as authViews

from .views import talks, participant

urlpatterns = [
    path('', talks.ProgrammeView.as_view(), name='default'),
    path('<int:year>/', talks.ProgrammeView.as_view(), name='programme'),
    path('<int:year>/participants', participant.ListView.as_view(), name='participants'),
    path('talk/<int:id>/', talks.SlotView.as_view(), name='slot'),

    path('participant/<slug:username>/', participant.ParticipantView.as_view(), name='account'),
    path('login', authViews.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout', authViews.LogoutView.as_view(template_name='core/logout.html', next_page='default'), name='logout'),
]

