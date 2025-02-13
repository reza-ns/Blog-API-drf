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


