from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache

from .models import HomeSite, HeaderSite


@receiver([post_delete, post_save], sender=[HomeSite])
def clear_cache(sender, instance, **kwargs):
    get_home_site_cache = cache.keys("*home_site_cache*")
    get_header_site_cache = cache.keys("*header_site_cache*")

    if get_home_site_cache:
        cache.delete_pattern("*home_site_cache*")
    if get_header_site_cache:
        cache.delete_pattern("*header_site_cache*")


@receiver([post_delete, post_save], sender=HeaderSite)
def clear_cache(sender, instance, **kwargs):
    get_header_site_cache = cache.keys("*header_site_cache*")

    if get_header_site_cache:
        cache.delete_pattern("*header_site_cache*")
