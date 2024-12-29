from django.db import models
from slugify import slugify


class BaseSlugField(models.Model):
    def save(self, *args, **kwargs):
        """
        Автоматически создает slug на основе поля title / username
        """
        if hasattr(self, 'username') and self.username:
            self.slug = slugify(self.username)
        elif hasattr(self, 'title') and self.title:
            self.slug = slugify(self.title)
        else:
            raise ValueError("Не удалось создать slug: отсутствует поле username или title")
        super().save(*args, **kwargs)

    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True
