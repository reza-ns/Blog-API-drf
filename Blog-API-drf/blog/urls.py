from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework import routers
from .api import views

app_name = 'blog'

router = routers.SimpleRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')


urlpatterns = [
    path('category/<slug:category_slug>',
         cache_page(60, key_prefix='category_list')(views.CategoryView.as_view()), name='category'),
    path('tag/<slug:tag_slug>',
         cache_page(60, key_prefix='tag_list')(views.TagView.as_view()), name='tag'),
    path('articles/<slug:article_slug>/comment', views.CommentView.as_view(), name='comment'),
]

urlpatterns += router.urls