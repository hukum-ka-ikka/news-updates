from django.db import models

class FeedModel(models.Model):
    title = models.TextField()
    summary = models.TextField()
    published = models.DateTimeField()
    image = models.URLField()
    link = models.URLField(unique=True)
    shortened_link = models.URLField()

    def __str__(self):
        return self.title 