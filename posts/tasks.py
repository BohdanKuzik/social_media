from celery import shared_task
from django.utils import timezone


@shared_task
def publish_scheduled_post(post_id):
    from posts.models import Post
    try:
        post = Post.objects.get(id=post_id)
        if post.scheduled_time <= timezone.now():
            post.publish()
    except Post.DoesNotExist:
        return f"Post {post_id} does not exist"
