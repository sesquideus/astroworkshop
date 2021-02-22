from django.urls import path

from .views import talks

urlpatterns = [
    path('', talks.ProgrammeView.as_view(), name='default'),
    path('<int:year>/', talks.ProgrammeView.as_view(), name='programme'),
    path('talk/<int:id>/', talks.SlotView.as_view(), name='slot'),
]

