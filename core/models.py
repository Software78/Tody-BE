from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    userId = models.IntegerField(default=0, blank=False, null=False)
    def __str__(self):
        return self.title