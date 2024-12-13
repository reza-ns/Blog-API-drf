from django.urls import path
from . import views

app_name = 'accounts-api'


urlpatterns = [
    path('<int:user_id>', views.UserView.as_view(), name='user')
]