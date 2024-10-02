from django.urls import path
from . import views


app_name = 'api'


urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='post_list'),
    path('articles/<slug:article_slug>', views.ArticleDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>', views.CategoryView.as_view(), name='post_detail'),
    path('tag/<slug:tag_slug>', views.TagView.as_view(), name='post_detail'),
]