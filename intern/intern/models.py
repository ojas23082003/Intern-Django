from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    address = models.TextField()
    usertype = models.CharField(null=True, blank=True, max_length=250)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return (self.user.username)