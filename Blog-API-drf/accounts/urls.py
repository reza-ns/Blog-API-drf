from django.urls import path, include
from .api import views

app_name = 'accounts'


urlpatterns = [
    path('<int:user_id>', views.UserView.as_view(), name='user'),
    path('auth/', views.AuthView.as_view(), name='auth'),
]