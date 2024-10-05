from django.db.models import F
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import now

from courses.models import Like, DiscountCourse


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


@receiver(post_save, sender=DiscountCourse)
def delete_discount_course(sender, instance, **kwargs):
    if instance.expired_date < now():
        instance.delete()
