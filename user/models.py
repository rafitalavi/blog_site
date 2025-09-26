from django.contrib.auth.models import User
from django.db import models
from django.utils.deconstruct import deconstructible
import os

@deconstructible
class UploadToPathAndRename:
    def __init__(self, path):
        self.path = path  # store base path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'profile_image.{ext}'
        # Construct path: accounts/<user_id>/images/
        full_path = os.path.join(self.path, str(instance.user.id), 'images')
        return os.path.join(full_path, filename)

# Instantiate with a base path
file_path = UploadToPathAndRename('accounts')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=file_path, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
