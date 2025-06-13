from django.db.models.signals import post_save
from django.dispatch import receiver

from posts.models import Post
from posts.tasks import publish_scheduled_post


@receiver(post_save, sender=Post)
def schedule_post_publication(sender, instance, created, **kwargs):
    if instance.scheduled_time and not instance.published:
        publish_scheduled_post.apply_async(
            args=[instance.id],
            eta=instance.scheduled_time
        )
