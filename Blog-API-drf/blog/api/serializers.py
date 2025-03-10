from rest_framework import serializers
from blog import models


class CommentRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'body', 'parent', 'create_date', 'user')


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_categories')
    tags = serializers.SerializerMethodField('get_tags')
    comments = CommentRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = models.Article
        fields = ('title', 'content', 'category', 'tags', 'create_date', 'thumbnail', 'comments')

    def get_tags(self, obj):
        tag_names = []
        for tag in obj.tags.all():
            tag_names.append(tag.name)
        return tag_names

    def get_categories(self, obj):
        categories = []
        for cat in obj.category.all():
            categories.append(cat.name)
        return categories


class ArticleListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_categories')

    class Meta:
        model = models.Article
        fields = ('title', 'category', 'thumbnail')

    def get_categories(self, obj):
        categories = []
        for cat in obj.category.all():
            categories.append(cat.name)
        return categories


class ArticleMakeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = (
            'title', 'status', 'content','category', 'tags', 'is_paid', 'thumbnail'
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('body', 'parent')




