from django.urls import path
from rest_framework import routers
from . import views


app_name = 'blog-api'

router = routers.SimpleRouter()
router.register(r'articles', views.ArticleViewSet)


urlpatterns = [
    path('category/<slug:category_slug>', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.TagView.as_view(), name='tag'),
    path('articles/<slug:article_slug>/comment', views.CommentView.as_view(), name='comment'),
]

urlpatterns += router.urls

