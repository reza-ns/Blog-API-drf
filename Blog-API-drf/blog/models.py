from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True)
    parent = models.ForeignKey('Category', on_delete=models.PROTECT,
                               null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISH = 'publish'

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISH, 'Publish')
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80, unique=True, allow_unicode=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    category = models.ManyToManyField('Category', related_name='articles')
    user = models.ForeignKey(User, blank=True, on_delete=models.PROTECT, related_name='articles')
    tags = models.ManyToManyField('Tag', related_name='articles')
    thumbnail = models.ImageField(upload_to='articles/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField()
    parent = models.ForeignKey('Comment', on_delete=models.PROTECT,
                               null=True, blank=True, related_name='replies')
    create_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    article = models.ForeignKey('Article', on_delete=models.PROTECT, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='comments')

    def __str__(self):
        return f"{self.id}"


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    user = models.ForeignKey(User, blank=True, on_delete=models.PROTECT, related_name='tags')

    def __str__(self):
        return self.name
