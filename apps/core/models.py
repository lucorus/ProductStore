from django.db import models
from slugify import slugify


class BaseSlugField(models.Model):
    def save(self, *args, **kwargs):
        """
        Автоматически создает slug на основе поля title / username
        """
        try:
            self.slug = slugify(self.username)
        except:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True
