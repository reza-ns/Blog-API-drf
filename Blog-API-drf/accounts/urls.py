from django.urls import path, include
from .api import views

app_name = 'accounts'


urlpatterns = [
    path('<int:user_id>', views.UserView.as_view(), name='user'),
    path('register', views.UserRegisterView.as_view(), name='user_register'),
    path('login', views.UserLoginView.as_view(), name='user_login'),
]