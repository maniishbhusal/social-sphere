from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ai_response = models.TextField()
    prompt = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.id}"