from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models. CharField(max_length=250, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='arthub/', default='../default_profile_w82a0x'
    )

    class Meta:
        """
        Meta class to the Profile model class
        """
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Creating a profile when user is added function
    """
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
