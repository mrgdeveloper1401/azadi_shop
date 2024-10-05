from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save

from courses.models import Like


@receiver(post_save, sender=Like)
def handle_like_dislike(sender, instance, created, **kwargs):
    course = instance.course
    if created and not instance.dislike:
        course.total_like = F('total_like') + 1
        course.save()
    elif not created and instance.dislike:
        course.total_like = F('total_like') - 1
        course.save()
        instance.delete()

