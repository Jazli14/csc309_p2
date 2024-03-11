from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import test_ping, CalendarListCreate, CalendarRetrieveUpdateDestroy 

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_ping),
    path('calendar/', CalendarListCreate.as_view(), name='calendar-list'),
    path('calendar/<int:pk>/', CalendarRetrieveUpdateDestroy.as_view(), name='calendar-detail'),
]