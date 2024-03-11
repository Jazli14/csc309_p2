from django.urls import path
from .views import test_ping, CalendarListCreate, CalendarRetrieveUpdateDestroy 

urlpatterns = [
    path('test/', test_ping),
    path('calendar/', CalendarListCreate.as_view(), name='calendar-list'),
    path('calendar/<int:pk>/', CalendarRetrieveUpdateDestroy.as_view(), name='calendar-detail'),
]
