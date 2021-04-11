from django.db import models


class ImageModel(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='images/')

