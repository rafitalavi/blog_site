from django.db import models
from django.utils.text import slugify
from django.utils.deconstruct import deconstructible
import datetime
import os

# ==========================
# File path generators
# ==========================

@deconstructible
class GenerateBlogImageFilePath:
    """Generates file path for blog images."""
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        title_slug = slugify(instance.title) if instance.title else "untitled"
        path = f'blog_image/{title_slug}/attachments'
        name = f'{title_slug}_attachments.{ext}'
        return os.path.join(path, name)

@deconstructible
class GenerateMetaImageFilePath:
    """Generates file path for meta images."""
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        title_slug = slugify(instance.title) if instance.title else "untitled"
        path = f'blog_image/{title_slug}/meta'
        name = f'{title_slug}_meta.{ext}'
        return os.path.join(path, name)

# Instantiate file path handlers
file_image = GenerateBlogImageFilePath()
file_meta_image = GenerateMetaImageFilePath()

# ==========================
# Blog Model
# ==========================

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.CharField(max_length=100, default='Admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    # ==========================
    #categories and subcategories
    # ==========================
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True, blank=True)

    # Images
    image = models.ImageField(upload_to=file_image, blank=True, null=True)
    meta_title = models.CharField(max_length=160, blank=True, null=True)
    meta_description = models.CharField(max_length=160, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_image = models.ImageField(upload_to=file_meta_image, blank=True, null=True)

    # ==========================
    # Save method: auto-generate slug
    # ==========================
    def save(self, *args, **kwargs):
        if not self.slug:
            # Ensure uniqueness using timestamp
            timestamp = str(int(datetime.datetime.now().timestamp()))
            self.slug = slugify(f"{self.title}-{timestamp}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Blogs"


class Category(models.Model):
    """
    Model representing a blog category.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    def save(self, *args, **kwargs):
        if not self.slug:
            timestamp = str(int(datetime.datetime.now().timestamp()))
            self.slug = slugify(f"{self.name}-{timestamp}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    """
    Model representing a subcategory linked to a parent category.
    """
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(
        Category, 
        related_name='subcategories', 
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            timestamp = str(int(datetime.datetime.now().timestamp()))
            self.slug = slugify(f"{self.name}-{timestamp}")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"

    def __str__(self):
        return f"{self.name} under {self.category.name}"