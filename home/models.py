from django.db import models
from django.utils.deconstruct import deconstructible
import os

# Utility to generate file paths for ImageField
@deconstructible
class GenerateAttachmentFilePath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # Use a safe version of the title for file paths
        task_title = instance.title.replace(" ", "_") if hasattr(instance, "title") and instance.title else "untitled"
        path = f'banner_images/{task_title}/attachments'
        name = f'{task_title}_attachments.{ext}'
        return os.path.join(path, name)

filePath = GenerateAttachmentFilePath()

# Contact Model
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# Banner Model
class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to=filePath, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Websetting Model
class Websetting(models.Model):
    title = models.CharField(max_length=200)  # required

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_map = models.TextField(blank=True, null=True)

    short_descriptions = models.CharField(max_length=255, blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_image = models.ImageField(upload_to="meta/", blank=True, null=True)
    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    fav_image = models.ImageField(upload_to="favicon/", blank=True, null=True)
    google_analytics_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title

