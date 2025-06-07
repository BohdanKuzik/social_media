from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Post
from .utils import schedule_post_publish

@receiver(post_save, sender=Post)
def post_create_handler(sender, instance, created, **kwargs):
    if created and not instance.published:
        schedule_post_publish(instance)