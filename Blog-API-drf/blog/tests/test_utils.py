from django.test import TransactionTestCase
from blog.utils import make_slug
from blog.models import Category


class TestUtilsMakeSlug(TransactionTestCase):
    """
    Things to test:
    - Is slugify correctly?
    - Is keep uniqueness when similar slug exist?
    """
    def test_slugify_value(self):
        category = Category(name='cat one')
        self.assertEqual(make_slug(category, 'name'), 'cat-one')

    def test_slug_uniqueness(self):
        cat1 = Category.objects.create(name='cat one')
        cat2 = Category(name='cat one')
        self.assertNotEqual(cat1.slug, make_slug(cat2, 'name'))