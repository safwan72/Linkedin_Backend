from django.db import models
from auth_api.models import UserProfile

# Create your models here.


class Connection(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="receiver"
    )
    date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User connection"
        db_table = "User connection"

    def __str__(self):
        return self.sender.user.email + " > Sent Request to " + self.receiver.user.email
