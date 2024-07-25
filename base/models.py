from django.db import models
from anchor.models.fields import BlobField

# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=100, null=True)
    count = models.IntegerField(null=True)


class Movie(models.Model):
    title = models.CharField(max_length=100)

    # A compulsory field that must be set on every instance
    # cover = BlobField()
    movie_cover = models.ImageField(blank=True, null=True)
    movie_posters = models.ImageField(blank=True, null=True)

    # An optional file that can be left blank
    # poster = BlobField(blank=True, null=True)