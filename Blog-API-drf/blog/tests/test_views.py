from unicodedata import category

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from blog import models

User = get_user_model()


class TestArticleViewSet(APITestCase):
    """
    Things to test:
    - test article list view
    - test article detail view
    - test that not published (draft) article not show
    - test that paid article not show for regular user
    - test create article with required fields
    - test not create article when non author user send request
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email = 'example@mail.com')
        cls.article = models.Article.objects.create(
            title='article one',
            content='article one content',
            user=cls.user,
            status=models.Article.STATUS_PUBLISH
        )

    def test_article_list(self):
        url = reverse('blog:article-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_article_detail(self):
        url = reverse('blog:article-detail', args=[self.article.slug])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_draft_article(self):
        self.article.status = models.Article.STATUS_DRAFT
        self.article.save()
        url = reverse('blog:article-detail', args=[self.article.slug])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_paid_article_permission(self):
        self.article.is_paid = True
        self.article.save()
        url = reverse('blog:article-detail', args=[self.article.slug])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article(self):
        url = reverse('blog:article-list')
        data = {
            'title': 'article test',
            'content': 'article test content',
        }
        self.user.role = User.UserRole.AUTHOR
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_article_permission(self):
        url = reverse('blog:article-list')
        data = {
            'title': 'article test',
            'content': 'article test content',
        }
        self.client.force_authenticate(user=self.user)
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TestCategoryView(APITestCase):
    """
    Things to test:
    - test url work correctly
    - test that view response has correct value count
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='example@mail.com')
        cls.category = models.Category.objects.create(name='cat one')
        cls.url = reverse('blog:category', args=[cls.category.slug])
        for i in range(10):
            cls.article = models.Article.objects.create(
                title=f"article{i}",
                content="sample content",
                user=cls.user,
                status=models.Article.STATUS_PUBLISH,
            )
            cls.article.category.add(cls.category)


    def test_category_url(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_category_articles_count(self):
        res = self.client.get(self.url)
        self.assertEqual(res.json()['count'], 10)


class TestCommentView(APITestCase):
    """
    Things to test:
    - test comment create url
    - test not authenticated user can't create comment
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='example@mail.com')
        cls.article = models.Article.objects.create(
            title='article one',
            content='article one content',
            user=cls.user,
            status=models.Article.STATUS_PUBLISH
        )
        cls.url = reverse('blog:comment', args=[cls.article.slug])

    def test_comment_create(self):
        data = {'body':'sample comment','user':self.user, 'article':self.article}
        self.client.force_authenticate(user=self.user)
        res = self.client.post(self.url, data=data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_comment_create_permission(self):
        data = {'body': 'sample comment', 'user': self.user, 'article': self.article}
        res = self.client.post(self.url, data=data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

