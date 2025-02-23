from django.utils.decorators import method_decorator
from rest_framework import mixins, viewsets
from django.views.decorators.cache import cache_page

from main_settings.models import HeaderSite, ContactUs, Newsletter, HomeSite, TopRankProfessor
from . import serializers


class HeaderSiteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HeaderSite.objects.filter(is_active=True).only('title')
    serializer_class = serializers.ListHeaderSiteSerializer

    @method_decorator(cache_page(20 * 60, key_prefix='header_site_cache'))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


class ContactUsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactUs.objects.all().only("full_name", "mobile_phone", "description")
    serializer_class = serializers.ContactUsSerializer


class NewsLatterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Newsletter.objects.all().only("email")
    serializer_class = serializers.NewsletterSerializer


class HomeSiteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HomeSite.objects.filter(is_main_settings=True).defer(
        "is_deleted", "deleted_at", "created_at", "updated_at", "is_main_settings"
    )
    serializer_class = serializers.HomeSiteSerializer

    @method_decorator(cache_page(20 * 60, key_prefix="home_site_cache"))
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


# class TopRankProfessorViewSet(ListModelMixin, GenericViewSet):
#     queryset = TopRankProfessor.objects.all()
#     serializer_class = TopRankProfessorSerializer
