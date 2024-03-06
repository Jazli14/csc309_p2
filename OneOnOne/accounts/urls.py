from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import test_endpoint, create_user_account, handle_contacts

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_endpoint, name='create_user'),
    path('users/', create_user_account),
    path('users/<int:user_id>/contacts/', handle_contacts, name='add_contact'),
    # path('users/<int:user_id>/contacts/<int:contact_id>/', get_contact, name='get_contact'),
    # path('users/<int:user_id>/contacts/<int:contact_id>/', update_contact, name='update_contact'),
    # path('users/<int:user_id>/contacts/<int:contact_id>/', delete_contact, name='delete_contact'),

]