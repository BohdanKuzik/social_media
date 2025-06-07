from django.utils import timezone
from celery import shared_task

from models import Post


@shared_task
def publish_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        if not post.published and post.scheduled_time <= timezone.now():
            post.published = True
            post.save()
            print(f"Post '{post.content[:25]}' published")
    except Post.DoesNotExist:
        print("Post does not exist.")
