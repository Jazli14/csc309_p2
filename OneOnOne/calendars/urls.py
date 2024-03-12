from django.urls import path
from .views import test_ping, CalendarListCreate, CalendarRetrieveUpdateDestroy, TimeBlocksListView, AddTimeBlockView, EditTimeBlockView, DeleteTimeBlockView 

urlpatterns = [
    path('test/', test_ping),
    path('calendar/', CalendarListCreate.as_view(), name='calendar-list'),
    path('calendar/<int:pk>/', CalendarRetrieveUpdateDestroy.as_view(), name='calendar-detail'),
    path('calendar/<int:calendar_id>/timeblocks/', TimeBlocksListView.as_view(), name='timeblocks-list'),
    path('calendar/<int:calendar_id>/timeblocks/add/', AddTimeBlockView.as_view(), name='add-timeblock'),
    path('timeblocks/<int:pk>/', EditTimeBlockView.as_view(), name='edit-timeblock'),
    path('timeblocks/<int:timeblock_id>/delete', DeleteTimeBlockView.as_view(), name='delete-timeblock'),
]