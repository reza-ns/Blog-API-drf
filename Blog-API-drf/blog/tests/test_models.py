from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from blog import models

User = get_user_model()


class TestCategoryModel(TestCase):
    """
    Things to test:
    - Can create category with name and slug?
    - Is slug created correctly?
    - Is the slug unique?
    - Does the __Str__ method behave as expected?
    """
    def setUp(self):
        self.cat = models.Category.objects.create(name='cat one')

    def test_create_category(self):
        self.assertTrue(models.Category.objects.filter(pk=self.cat.pk).exists())

    def test_slug_value(self):
        self.assertEqual(self.cat.slug, slugify(self.cat.name))

    def test_slug_uniqueness(self):
        cat2 = models.Category.objects.create(name=self.cat.name)
        self.assertNotEqual(cat2.slug, self.cat.slug)

    def test_str(self):
        self.assertEqual(str(self.cat), 'cat one')


class TestTagModel(TestCase):
    """
    Things to test:
    - Can create tag with name and slug and user?
    - Is slug created correctly?
    - Is the slug unique?
    - Does the __Str__ method behave as expected?
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email = 'example@mail.com')
        cls.tag = models.Tag.objects.create(name='tag one', user=cls.user)

    def test_create_tag(self):
        self.assertTrue(models.Tag.objects.filter(pk=self.tag.pk).exists())

    def test_slug_value(self):
        self.assertEqual(self.tag.slug, slugify(self.tag.name))

    def test_slug_uniqueness(self):
        tag2 = models.Tag.objects.create(name=self.tag.name, user=self.user)
        self.assertNotEqual(tag2.slug, self.tag.slug)

    def test_str(self):
        self.assertEqual(str(self.tag), 'tag one')


class TestArticleModel(TestCase):
    """
    Things to test:
    - Can create article with minimum requirement?
    - Is slug created correctly?
    - Is the slug unique?
    - Does the __Str__ method behave as expected?
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email = 'example@mail.com')
        cls.category = models.Category.objects.create(name='cat one', slug='cat-one')
        cls.tag = models.Tag.objects.create(name='tag one', slug='tag-one', user=cls.user)
        cls.article = models.Article.objects.create(
            title='article one',
            content='article one content',
            user=cls.user
        )
        cls.article.category.add(cls.category)
        cls.article.tags.add(cls.tag)

    def test_create_article(self):
        self.assertTrue(models.Article.objects.filter(pk=self.article.pk).exists())

    def test_slug_value(self):
        self.assertEqual(self.article.slug, slugify(self.article.title))

    def test_slug_uniqueness(self):
        article2 = models.Article.objects.create(
            title=self.article.title,
            content='article two content',
            user=self.user
        )
        article2.category.add(self.category)
        article2.tags.add(self.tag)

        self.assertNotEqual(article2.slug, self.article.slug)

    def test_str(self):
        self.assertEqual(str(self.article), 'article one')


class TestCommentModel(TestCase):
    """
    Things to test:
    - Can create article with minimum requirement?
    - Is comment accept parent?
    - Does the __Str__ method behave as expected?
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='example@mail.com')
        cls.category = models.Category.objects.create(name='cat one', slug='cat-one')
        cls.tag = models.Tag.objects.create(name='tag one', slug='tag-one', user=cls.user)
        cls.article = models.Article.objects.create(
            title='article one',
            content='article one content',
            user=cls.user
        )
        cls.article.category.add(cls.category)
        cls.article.tags.add(cls.tag)
        cls.comment = models.Comment.objects.create(
            body='comment content',
            article=cls.article,
            user=cls.user
        )

    def test_create_comment(self):
        self.assertTrue(models.Comment.objects.filter(pk=self.comment.pk).exists())

    def test_comment_parent_accept(self):
        comment2 = models.Comment.objects.create(
            body='comment2 content',
            article=self.article,
            user=self.user,
            parent=self.comment
        )
        self.assertEqual(comment2.parent, self.comment)

    def test_str(self):
        self.assertEqual(str(self.comment), '1')






















