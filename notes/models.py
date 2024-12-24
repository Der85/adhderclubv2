from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")

    class Meta:
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name

class Notes(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    title = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    tags = models.ManyToManyField(Tag, blank=True)
    is_completed = models.BooleanField(default=False)

    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return timezone.now() > self.due_date
        return False

    class Meta:
        ordering = ['due_date', '-priority', '-created']

    def __str__(self):
        return self.title