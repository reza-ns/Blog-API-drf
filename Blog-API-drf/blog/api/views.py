from rest_framework import generics
from rest_framework import viewsets
from django.utils.text import slugify
from blog import models
from . import serializers
from . import permissions


def make_slug(data):
    title = data.get('title')
    return slugify(title, allow_unicode=True)


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
        if self.action == 'list':
            return serializers.ArticleListSerializer
        elif self.action == 'retrieve':
            return serializers.ArticleRetrieveSerializer
        else:
            return serializers.ArticleMakeUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, slug=make_slug(self.request.data))


class CategoryView(generics.ListAPIView):
    serializer_class = serializers.ArticleListSerializer
    lookup_url_kwarg = 'category_slug'
    lookup_field = 'slug'

    def get_queryset(self):
        category = models.Category.objects.get(slug=self.kwargs['category_slug'])
        articles = (models.Article.objects.filter(category=category, status=models.Article.STATUS_PUBLISH)
                    .order_by('-create_date'))
        return articles


class TagView(generics.ListAPIView):
    serializer_class = serializers.ArticleListSerializer
    lookup_url_kwarg = 'tag_slug'
    lookup_field = 'slug'

    def get_queryset(self):
        tag = models.Tag.objects.get(slug=self.kwargs['tag_slug'])
        articles = tag.articles.filter(status=models.Article.STATUS_PUBLISH).order_by('-create_date')
        return articles



