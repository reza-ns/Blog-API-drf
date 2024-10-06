from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from blog import models
from . import serializers
from .permissions import IsAuthorOrReadOnly


class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class CategoryView(generics.ListAPIView):
    serializer_class = serializers.ArticleSerializer
    lookup_url_kwarg = 'category_slug'
    lookup_field = 'slug'

    def get_queryset(self):
        category = models.Category.objects.get(slug=self.kwargs['category_slug'])
        articles = models.Article.objects.filter(category=category)
        return articles


class TagView(generics.ListAPIView):
    serializer_class = serializers.ArticleSerializer
    lookup_url_kwarg = 'tag_slug'
    lookup_field = 'slug'

    def get_queryset(self):
        tag = models.Tag.objects.get(slug=self.kwargs['tag_slug'])
        articles = tag.articles.all()
        return articles



