from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import test_endpoint, create_user_account, modify_user_account, handle_contacts, user_login

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_endpoint, name='test_endpoint'),
    path('users/', create_user_account, name='create_user'),
    path('login/', user_login, name='user_login'),
    path('users/<int:user_id>/', modify_user_account, name='update_user'),
    path('users/<int:user_id>/contacts/', handle_contacts, name='handle_contacts'),

]