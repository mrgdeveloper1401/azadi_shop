from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from main_settings.models import TopRankStudent, Services, ContactUs, Newsletter, HeaderSite, HomeSite


class HeaderSiteSerializer(ModelSerializer):
    class Meta:
        model = HeaderSite
        fields = ['id', "title", "is_active"]


class TopRankSerializer(ModelSerializer):
    class Meta:
        model = TopRankStudent
        fields = ['id', "first_name", "last_name", "fields", "is_active"]


class ServiceSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    class Meta:
        model = Services
        fields = ['id', "title", "description", "is_active", "link", "image_url"]

    def get_image_url(self, obj):
        return obj.services_image.image_url


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class NewsletterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']

    def validate(self, attrs):
        if Newsletter.objects.filter(email=attrs['email']).exists():
            raise ValidationError("Your email is registered for the newsletter")
        return attrs


class HomeSiteSerializer(ModelSerializer):
    site_logo = SerializerMethodField()
    about_us_image = SerializerMethodField()
    slider_professor_image = SerializerMethodField()
    team_image = SerializerMethodField()
    slider_image = SerializerMethodField()
    awards_image = SerializerMethodField()

    class Meta:
        model = HomeSite
        exclude = ['created_at', "updated_at"]

    def get_site_logo(self, obj):
        return obj.site_logo.image_url

    def get_about_us_image(self, obj):
        return obj.about_us_image.image_url

    def get_slider_professor_image(self, obj):
        return obj.slider_professor_image.image_url

    def get_team_image(self, obj):
        return obj.team_image.image_url

    def get_slider_image(self, obj):
        return [i.image_url for i in obj.slider_image.all()]

    def get_awards_image(self, obj):
        return [i.image_url for i in obj.awards_image.all()]
