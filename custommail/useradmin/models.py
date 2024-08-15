from django.db import models
from django.contrib.auth.models import User

class MailHistory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Allow blank descriptions
    task_link = models.URLField(blank=True, null=True)  # Allow blank task link
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_mails')
    recipients = models.TextField()  # Store as comma-separated email addresses
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class MailImage(models.Model):
    mail = models.ForeignKey(MailHistory, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mail_images/')

    def __str__(self):
        return f"Image for {self.mail.title}"