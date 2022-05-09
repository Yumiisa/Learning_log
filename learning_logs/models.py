from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    """A topic user is learning on"""

    text = models.CharField(max_length=32)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        """returning string representation of model"""
        return self.text


class Entry(models.Model):
    """Something specific learned about topic"""

    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    text = models.CharField(max_length=400, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        return str(self.text)[:50] + "..."
