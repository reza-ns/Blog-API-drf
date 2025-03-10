from unicodedata import category

from django.test import TestCase
from django.contrib.auth import get_user_model
from blog import models
from blog.api import serializers


User = get_user_model()


class TestArticleRetrieveSerializer(TestCase):
    """
    Things to test:
    - Check all expected fields exists in result
    - Check serializer result data types are correct?
    - Check serializer returns expected data?
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='example@mail.com')
        cls.category = models.Category.objects.create(name='cat one')
        cls.tag = models.Tag.objects.create(name='tag one', user=cls.user)
        cls.article = models.Article.objects.create(
            title='article one',
            content='article one content',
            user=cls.user
        )
        cls.article.category.add(cls.category)
        cls.article.tags.add(cls.tag)

    def test_serializer_result_contain_expected_fields(self):
        data = serializers.ArticleRetrieveSerializer(instance=self.article).data
        self.assertEqual(
            data.keys(),
            {'title', 'content', 'category', 'tags', 'create_date', 'thumbnail', 'comments'}
        )

    def test_serializer_result_correct_data_types(self):
        data = serializers.ArticleRetrieveSerializer(instance=self.article).data
        self.assertIsInstance(data['title'], str)
        self.assertIsInstance(data['content'], str)
        self.assertIsInstance(data['category'], list)
        self.assertIsInstance(data['tags'], list)
        self.assertIsInstance(data['create_date'], str)
        self.assertIsInstance(data['comments'], list)

    def test_serialization(self):
        expected_data = {
            'title': 'article one',
            'content': 'article one content',
            'category': ['cat one'],
            'tags': ['tag one'],
            'create_date': self.article.create_date.isoformat().replace('+00:00', 'Z'),
            'thumbnail': None,
            'comments': []
        }
        data = serializers.ArticleRetrieveSerializer(instance=self.article).data
        self.assertEqual(data, expected_data)


class TestArticleMakeUpdateSerializer(TestCase):
    """
    Things to test:
    - test is valid data accepted or not.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='example@mail.com')
        cls.cat = models.Category.objects.create(name='cat one')
        cls.tag = models.Tag.objects.create(name='tag one', user=cls.user)
        cls.article = models.Article.objects.create(
            title= 'article zero',
            content= 'article sample content',
            user= cls.user
        )
        cls.article.category.add(cls.cat)
        cls.article.tags.add(cls.tag)

    def test_valid_data(self):
        valid_data = {
            'title': 'article one',
            'status': 'publish',
            'content': 'sample content',
            'category': [self.cat.pk],
            'tags': [self.tag.pk],
            'is_paid': True,
            'thumbnail': None
        }
        serializer  = serializers.ArticleMakeUpdateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_blank_field(self):
        invalid_data = {
            'title': '',
            'content': '',
            'category': [self.cat.pk],
            'tags': [self.tag.pk],
        }
        serializer = serializers.ArticleMakeUpdateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('content', serializer.errors)

    def test_invalid_data_missing_required_field(self):
        invalid_data = {
            'category': [self.cat.pk],
            'tags': [self.tag.pk],
        }
        serializer = serializers.ArticleMakeUpdateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertIn('content', serializer.errors)

    def test_serializer_update(self):
        updated_data = {
            'title': 'updated article',
            'status': 'publish',
            'content': 'updated content',
            'category': [self.cat.pk],
            'tags': [self.tag.pk],
        }
        serializer = serializers.ArticleMakeUpdateSerializer(self.article, data=updated_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.article.title, 'updated article')
        self.assertEqual(self.article.content, 'updated content')
        self.assertEqual(self.article.status, 'publish')

    def test_serializer_update_invalid_data(self):
        invalid_updated_data = {
            'title': 'a'*101,
            'status': 'publish',
            'content': 'updated content',
            'category': [self.cat.pk],
            'tags': [self.tag.pk],
        }
        serializer = serializers.ArticleMakeUpdateSerializer(self.article, data=invalid_updated_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_serializer_partial_update(self):
        partial_update_data = {'title': 'partial updated article'}
        serializer = serializers.ArticleMakeUpdateSerializer(self.article, data=partial_update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(self.article.title, 'partial updated article')
        self.assertEqual(self.article.content, 'article sample content')
        self.assertEqual(self.article.id, 1)
        self.assertEqual(self.article.user.id, 1)

    def test_serializer_partial_update_invalid_data(self):
        invalid_partial_update_data = {'title': 'a'*101}
        serializer = serializers.ArticleMakeUpdateSerializer(
            self.article, data=invalid_partial_update_data, partial=True
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
