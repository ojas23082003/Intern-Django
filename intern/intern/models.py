from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    address = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return (self.user.username)

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    summary = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title