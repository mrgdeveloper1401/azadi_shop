from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from main_settings.models import TopRankStudent, ContactUs, Newsletter, HeaderSite, HomeSite, TopRankProfessor


class HeaderSiteSerializer(ModelSerializer):
    class Meta:
        model = HeaderSite
        fields = ['id', "title", "is_active"]


class TopRankSerializer(ModelSerializer):
    class Meta:
        model = TopRankStudent
        fields = ['id', "first_name", "last_name", "fields", "is_active"]


# class ServiceSerializer(ModelSerializer):
#     image_url = SerializerMethodField()
#
#     class Meta:
#         model = Services
#         fields = ['id', "title", "description", "is_active", "link", "image_url"]
#
#     def get_image_url(self, obj):
#         return obj.services_image.image_url


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
    slider_professor_image = SerializerMethodField()
    team_image = SerializerMethodField()
    slider_image = SerializerMethodField()
    awards_image = SerializerMethodField()

    class Meta:
        model = HomeSite
        exclude = ['created_at', "updated_at"]

    def get_site_logo(self, obj):
        return obj.site_logo.url if obj.site_logo else None

    def get_slider_professor_image(self, obj):
        img = [i.image_url for i in obj.slider_professor_image.all()]
        return img

    def get_team_image(self, obj):
        img = [i.image_url for i in obj.team_image.all()]
        return img

    def get_slider_image(self, obj):
        return [i.image_url for i in obj.slider_image.all()]

    def get_awards_image(self, obj):
        return [i.image_url for i in obj.awards_image.all()]


class TopRankProfessorSerializer(ModelSerializer):
    professor_image = SerializerMethodField()

    class Meta:
        model = TopRankProfessor
        fields = ['field_title', "full_name", "professor_image"]

    def get_professor_image(self, obj):
        return obj.professor_image.url if obj.professor_image else None
