from rest_framework import serializers
from blog import models


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ('title', 'content', 'category', 'create_date', 'tags', 'thumbnail')
