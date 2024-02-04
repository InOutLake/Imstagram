from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import os

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    small_description = models.TextField(max_length=150, 
                                         default="Remember to add small description to the image later...")
    full_description = models.TextField(max_length=2000, default="Remember to add description to your image later...")
    image_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True)
    is_favorite = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image:
            self.image.name = f'{self.image_owner.username}/{os.path.basename(self.image.name)}'
        super().save(*args, **kwargs)
