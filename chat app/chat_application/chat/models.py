from django.db import models

# Create your models here.
# chat/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.username

class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}: {self.content}'
