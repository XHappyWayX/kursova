from django.urls import path
from .views import GetDataView, CreateView, UpdateDeleteView
from .auth_view import RegisterUserView, TokenAuthView

urlpatterns = [
    path('api-accountant/', GetDataView().as_view(), name='get_data'),
    path('token-auth/', TokenAuthView.as_view(), name='token_auth'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('api-worker/', CreateView.as_view(), name='create'),
    path('api-worker/<int:pk>/', UpdateDeleteView.as_view(), name='update_delete'),
]