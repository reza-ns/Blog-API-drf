from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework import viewsets
from blog import models
from . import serializers
from . import permissions


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = models.Article.objects.filter(status=models.Article.STATUS_PUBLISH).order_by('-create_date')
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [permissions.IsAuthorOrReadOnly]
        elif self.action == 'retrieve':
            permission_classes = [permissions.IsSubscriberOrOwner]
        else:
            permission_classes = [permissions.IsAuthorOrReadOnly, permissions.IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.ArticleListRetrieveSerializer
        else:
            return serializers.ArticleMakeUpdateSerializer


class CategoryView(generics.ListAPIView):
    serializer_class = serializers.ArticleListRetrieveSerializer
    lookup_url_kwarg = 'category_slug'
    lookup_field = 'slug'

    def get_queryset(self):
        category = models.Category.objects.get(slug=self.kwargs['category_slug'])
        articles = (models.Article.objects.filter(category=category, status=models.Article.STATUS_PUBLISH)
                    .order_by('-create_date'))
        return articles


class TagView(generics.ListAPIView):
    serializer_class = serializers.ArticleListRetrieveSerializer
    lookup_url_kwarg = 'tag_slug'
    lookup_field = 'slug'

    def get_queryset(self):
        tag = models.Tag.objects.get(slug=self.kwargs['tag_slug'])
        articles = tag.articles.filter(status=models.Article.STATUS_PUBLISH).order_by('-create_date')
        return articles



