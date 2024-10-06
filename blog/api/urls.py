from django.urls import path
from rest_framework import routers
from . import views


app_name = 'api'

router = routers.SimpleRouter()
router.register(r'articles', views.ArticleViewSet)

urlpatterns = [
    path('category/<slug:category_slug>', views.CategoryView.as_view(), name='post_detail'),
    path('tag/<slug:tag_slug>', views.TagView.as_view(), name='post_detail'),
]

urlpatterns += router.urls

