from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import CategoryNode, Post


@receiver([post_save, post_delete], sender=CategoryNode)
def clear_category_cache(sender, instance, **kwargs):
    get_category_cache_list = cache.keys("*category_list_cache*")
    get_category_cache_retrieve = cache.keys("*category_retrieve_cache*")

    if get_category_cache_list:
        cache.delete_pattern(get_category_cache_list)
    if get_category_cache_retrieve:
        cache.delete_pattern(get_category_cache_retrieve)


@receiver([post_save, post_delete], sender=Post)
def clear_post_list_cache(sender, instance, **kwargs):
    get_post_cache = cache.keys("*post_list_cache*")
    get_post_cache_retrieve = cache.keys("*post_retrieve_cache*")

    if get_post_cache:
        cache.delete_pattern(get_post_cache)
    if get_post_cache_retrieve:
        cache.delete_pattern(get_post_cache_retrieve)
