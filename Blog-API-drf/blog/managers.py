from django.db import models
from django.db.utils import IntegrityError
from django.utils.text import slugify
import random


class MakeSlugManager(models.Manager):
    def create(self, **kwargs):
        if kwargs.get('title'):
            try:
                kwargs['slug'] = self.make_slug(kwargs['title'])
            except IntegrityError:
                kwargs['slug'] = self.make_slug(kwargs['title']) + '-' + str(random.randint(1000, 9999))
        elif kwargs.get('name'):
            try:
                kwargs['slug'] = self.make_slug(kwargs['name'])
            except IntegrityError:
                kwargs['slug'] = self.make_slug(kwargs['name']) + '-' + str(random.randint(1000, 9999))
        return super().create(**kwargs)

    def make_slug(self, name):
        return slugify(name, allow_unicode=True)