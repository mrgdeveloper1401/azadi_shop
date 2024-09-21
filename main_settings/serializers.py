from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.utils.translation import gettext_lazy as _

from main_settings.models import Footer, FooterAddress, TopRankStudent, Slider, Services, FooterSocial, Awards, AboutUs, \
    ContactUs, SiteLogo, Newsletter, HeaderSite, SliderProfessorImages, SliderProfessorImages


class HeaderSiteSerializer(ModelSerializer):
    class Meta:
        model = HeaderSite
        fields = '__all__'


class FooterSerializer(ModelSerializer):
    image_url = SerializerMethodField()
    footer_address = SerializerMethodField()

    class Meta:
        model = Footer
        exclude = ['footer_logo']

    def get_image_url(self, obj):
        return obj.footer_logo.image_url

    def get_footer_address(self, obj):
        return [i.address for i in obj.footer_address.all()]


class FooterSocialSerializer(ModelSerializer):
    class Meta:
        model = FooterSocial
        fields = '__all__'


class FooterAddressSerializer(ModelSerializer):
    class Meta:
        model = FooterAddress
        fields = '__all__'


class TopRankSerializer(ModelSerializer):
    class Meta:
        model = TopRankStudent
        fields = '__all__'


class SliderSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = Slider
        exclude = ['slider_image']

    def get_image_url(self, obj):
        return [i.image_url for i in obj.slider_image.all()]


class ServiceSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = Services
        exclude = ['services_image']

    def get_image_url(self, obj):
        return obj.services_image.image_url


class AwardsSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = Awards
        exclude = ['awards_image']

    def get_image_url(self, obj):
        return [i.image_url for i in obj.awards_image.all()]


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class SiteLogoSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = SiteLogo
        exclude = ['logo']

    def get_image_url(self, obj):
        return obj.logo.image_url


class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

    def validate(self, attrs):
        if Newsletter.objects.filter(email=attrs['email']).exists():
            raise ValidationError("Your email is registered for the newsletter")
        return attrs


class SliderProfessorImageSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = SliderProfessorImages
        exclude = ['professor_image']

    def get_image_url(self, obj):
        return [i.image_url for i in obj.professor_image.all()]


class AboutUsSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = AboutUs
        exclude = ['about_us_image']

    def get_image_url(self, obj):
        return obj.about_us_image.image_url
