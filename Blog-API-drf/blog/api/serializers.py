from rest_framework import serializers
from blog import models


class ArticleListRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Article
        fields = ['title', 'content', 'category', 'tags', 'create_date', 'thumbnail']


class ArticleMakeUpdateSerializer(serializers.ModelSerializer):
    # slug = serializers.SlugField(initial=)

    class Meta:
        model = models.Article
        fields = (
            'title', 'slug', 'status', 'content','category', 'tags', 'is_paid', 'user', 'thumbnail'
        )
