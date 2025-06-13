from celery import shared_task
from django.utils import timezone

from posts.models import Post

print("tasks works 1")


@shared_task
def publish_scheduled_post(post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.scheduled_time <= timezone.now():
            post.publish()
    except Post.DoesNotExist:
        return f"Post {post_id} does not exist"
    print("tasks works 2")
