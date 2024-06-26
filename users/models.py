from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User,AbstractBaseUser
from autoslug import AutoSlugField
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=40)
    image = models.ImageField(upload_to="media")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='blog_posts')
    
    def total_likes(self):
        return self.likes.count()
    

    def __str__(self):
        return str(self.title)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)
    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

class FriendRequest(models.Model):
    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user_requests', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)