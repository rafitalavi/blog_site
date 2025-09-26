from django.db import models 
from django.utils.deconstruct import deconstructible

import os
# Create your models here.
@deconstructible
@deconstructible
class GenerateAttachmentFilePath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        task_title = instance.title if instance.title else "untitled"
        path = f'banner_images/{task_title}/attachments'
        name = f'{task_title}_attachments.{ext}'
        return os.path.join(path, name)


filePath = GenerateAttachmentFilePath()
# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
class Banner(models.Model):
    title = models.CharField(max_length=200 ,blank=False ,null=False)
    subtitle = models.CharField(max_length=300 ,blank=True ,null=True)
    image = models.ImageField(upload_to=filePath, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title