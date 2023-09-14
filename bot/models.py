from django.db import models

class Conversation(models.Model):
    user_email = models.EmailField()
    message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_email} - {self.timestamp}'
    
class Student(models.Model):
    email = models.EmailField(unique=True)
    admission_number = models.CharField(max_length=20)
    fee_balance = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.email