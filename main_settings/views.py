from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from main_settings.models import SiteLogo, SliderProfessorImages, Slider, TopRankStudent, HeaderSite, AboutUs, Awards, \
    Newsletter, FooterSocial, Footer, FooterAddress, ContactUs, Services
from main_settings.serializers import FooterSerializer, FooterSocialSerializer, FooterAddressSerializer, \
    AboutUsSerializer, ContactUsSerializer, SliderSerializer, SliderProfessorImageSerializer, AwardsSerializer, \
    SiteLogoSerializer, HeaderSiteSerializer, ServiceSerializer, NewsletterSerializer, TopRankSerializer


class SiteLogoViewSet(ReadOnlyModelViewSet):
    queryset = SiteLogo.objects.filter(is_active=True).select_related("logo")
    serializer_class = SiteLogoSerializer


class SliderProfessorImageViewSet(ReadOnlyModelViewSet):
    queryset = SliderProfessorImages.objects.filter(is_active=True).prefetch_related('professor_image')
    serializer_class = SliderProfessorImageSerializer


class SliderViewSet(ReadOnlyModelViewSet):
    queryset = Slider.objects.filter(is_active=True).prefetch_related("slider_image")
    serializer_class = SliderSerializer


class TopRankStudentViewSet(ReadOnlyModelViewSet):
    queryset = TopRankStudent.objects.filter(is_active=True)
    serializer_class = TopRankSerializer


class HeaderSiteViewSet(ReadOnlyModelViewSet):
    queryset = HeaderSite.objects.filter(is_active=True)
    serializer_class = HeaderSiteSerializer


class AboutUsViewSet(ReadOnlyModelViewSet):
    queryset = AboutUs.objects.filter(is_active=True).select_related('about_us_image')
    serializer_class = AboutUsSerializer


class AwardsViewSet(ReadOnlyModelViewSet):
    queryset = Awards.objects.filter(is_active=True).prefetch_related('awards_image')
    serializer_class = AwardsSerializer


class NewsletterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer


class FooterViewSet(ReadOnlyModelViewSet):
    queryset = Footer.objects.filter(is_active=True).select_related('footer_logo').prefetch_related('footer_address')
    serializer_class = FooterSerializer


class FooterSocialViewSet(ReadOnlyModelViewSet):
    queryset = FooterSocial.objects.filter(is_active=True)
    serializer_class = FooterSocialSerializer


class FooterAddressViewSet(ReadOnlyModelViewSet):
    queryset = FooterAddress.objects.filter(is_active=True)
    serializer_class = FooterAddressSerializer


class ContactUsViewSet(CreateModelMixin, GenericViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer


class ServicesViewSet(ReadOnlyModelViewSet):
    queryset = Services.objects.filter(is_active=True).select_related("services_image")
    serializer_class = ServiceSerializer
