from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from main_settings.models import TopRankStudent, HeaderSite, ContactUs, Services, Newsletter, HomeSite
from main_settings.serializers import (ContactUsSerializer, HeaderSiteSerializer, ServiceSerializer,
                                       NewsletterSerializer, TopRankSerializer, HomeSiteSerializer)


class TopRankStudentViewSet(ReadOnlyModelViewSet):
    queryset = TopRankStudent.objects.filter(is_active=True)
    serializer_class = TopRankSerializer


class HeaderSiteViewSet(ReadOnlyModelViewSet):
    queryset = HeaderSite.objects.filter(is_active=True)
    serializer_class = HeaderSiteSerializer


class ContactUsViewSet(CreateModelMixin, GenericViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class ServicesViewSet(ReadOnlyModelViewSet):
    queryset = Services.objects.filter(is_active=True).select_related("services_image")
    serializer_class = ServiceSerializer


class NewsLatterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class HomeSiteViewSet(ReadOnlyModelViewSet):
    queryset = HomeSite.objects.filter(is_active=True).select_related('site_logo', "about_us_image",
                                                                      "slider_professor_image",
                                                                      "team_image").prefetch_related("team_image",
                                                                                                     "slider_image")
    serializer_class = HomeSiteSerializer
