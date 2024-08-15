from django.db import models
from django.contrib.auth.models import User

class MailHistory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    task_link = models.URLField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_mails')
    recipients = models.TextField()  # Store as comma-separated email addresses
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
