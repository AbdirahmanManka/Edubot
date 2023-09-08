from django.db import models

class Conversation(models.Model):
    user_email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_email} - {self.timestamp}'
