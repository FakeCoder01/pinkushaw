from django.db import models
from core.models import Profile, Match
# Create your models here.




class Chat(models.Model):
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="match_chat")
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="chat_sender")
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat/images/', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.profile.full_name