from rest_framework import generics
from blog import models
from . import serializers


class ArticleListView(generics.ListAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    lookup_url_kwarg = 'article_slug'
    lookup_field = 'slug'


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



