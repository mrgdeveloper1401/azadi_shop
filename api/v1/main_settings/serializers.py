from rest_framework import serializers
from main_settings.models import ContactUs, Newsletter, HeaderSite, HomeSite, TopRankProfessor, BusinessAddress, \
    ContactUsSocial
from shop import status_code


class ListHeaderSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderSite
        fields = ["title"]


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        exclude = ['created_at', 'updated_at', "is_deleted", "deleted_at"]


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']

    def validate(self, attrs):
        if Newsletter.objects.filter(email=attrs['email']).exists():
            raise status_code.OBJECT_ALREADY_EXISTS
        return attrs


class HomeSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSite
        exclude = ['is_deleted', "deleted_at", "created_at", "updated_at", "is_main_settings"]


class TopRankProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopRankProfessor
        fields = ['field_title', "full_name", "professor_image_url"]


class BusinessAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAddress
        fields = ['location_lat', "location_long"]


class ContactUsSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsSocial
        fields = ['social_link', "social_name"]
