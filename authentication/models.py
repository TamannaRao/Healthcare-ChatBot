# authentication/models.py
from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_chathistory_set')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

