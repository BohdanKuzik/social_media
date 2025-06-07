from django.utils.timezone import now

from tasks import publish_post


def schedule_post_publish(post):
    publish_time = post.scheduled_time
    if publish_time > now():
        publish_post.apply_async(args=[post.id], eta=publish_time)
    else:
        publish_post.delay(post.id)
