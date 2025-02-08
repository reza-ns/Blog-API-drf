from django.utils.text import slugify

def make_slug(instance, source_field):
    slug = slugify(getattr(instance, source_field))
    unique_slug = slug
    counter = 1
    while instance.__class__.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug



