from django.db import models
from auth_api.models import UserProfile

# Create your models here.
class Thread(models.Model):
    first_member = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="member_first"
    )
    second_member = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="member_second"
    )

    def __str__(self):
        return (
            f"{self.first_member.user.username} <> {self.second_member.user.username}"
        )


class Chat(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    time_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)
    # file         = models.FileField(upload_to = 'chat/', null = True, blank = True, max_length = 10485760)
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="msg_sent"
    )

    def __str__(self):
        return f"{self.sender.user.username} chats"

    class Meta:
        ordering = ("-time_created",)
