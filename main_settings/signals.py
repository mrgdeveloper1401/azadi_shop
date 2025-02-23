from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.core.cache import cache

from .models import HomeSite, HeaderSite, TopRankProfessor, BusinessAddress, ContactUsSocial


@receiver([post_delete, post_save], sender=[HomeSite])
def clear_cache_home_site(sender, instance, **kwargs):
    get_home_site_cache = cache.keys("*home_site_cache*")
    get_header_site_cache = cache.keys("*header_site_cache*")

    if get_home_site_cache:
        cache.delete_pattern("*home_site_cache*")
    if get_header_site_cache:
        cache.delete_pattern("*header_site_cache*")


@receiver([post_delete, post_save], sender=HeaderSite)
def clear_cache_header_site(sender, instance, **kwargs):
    get_header_site_cache = cache.keys("*header_site_cache*")

    if get_header_site_cache:
        cache.delete_pattern("*header_site_cache*")


@receiver([post_delete, post_save], sender=TopRankProfessor)
def clear_cache_top_teacher(sender, instance, **kwargs):
    get_header_site_cache = cache.keys("*top_teacher_cache*")

    if get_header_site_cache:
        cache.delete_pattern("*top_teacher_cache*")


@receiver([post_delete, post_save], sender=BusinessAddress)
def clear_cache_business_address(sender, instance, **kwargs):
    get_header_site_cache = cache.keys("*business_address_cache*")
    if get_header_site_cache:
        cache.delete_pattern("*business_address_cache*")


@receiver([post_delete, post_save], sender=ContactUsSocial)
def clear_cache_social(sender, instance, **kwargs):
    get_header_site_cache = cache.keys("*social_cache*")
    if get_header_site_cache:
        cache.delete_pattern("*social_cache*")
