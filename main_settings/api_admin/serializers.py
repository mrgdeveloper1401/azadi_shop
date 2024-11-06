from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import HeaderSite, HomeSite, ContactUs, TopRankStudent, TopRankProfessor, Newsletter


class AdminHeaderSiteSerializer(ModelSerializer):
    class Meta:
        model = HeaderSite
        fields = '__all__'


class HomeSiteSerializer(ModelSerializer):
    slider_images = SerializerMethodField()
    about_us_images = SerializerMethodField()
    site_logos = SerializerMethodField()
    slider_professor_images = SerializerMethodField()
    awards_images = SerializerMethodField()
    team_images = SerializerMethodField()

    class Meta:
        model = HomeSite
        fields = '__all__'

    def get_slider_images(self, obj):
        img = [i.image_url if i.image_url else None for i in obj.slider_image.all()]
        return img

    def get_about_us_images(self, obj):
        img = [i.image_url if i.image_url else None for i in obj.about_us_image.all()]
        return img

    def get_site_logos(self, obj):
        return obj.site_logo.image.url if obj.site_logo else None

    def get_slider_professor_images(self, obj):
        img = [i.image_url if i.image_url else None for i in obj.slider_professor_image.all()]
        return img

    def get_awards_images(self, obj):
        img = [i.image_url if i.image_url else None for i in obj.awards_image.all()]
        return img

    def get_team_images(self, obj):
        img = [i.image_url if i.image_url else None for i in obj.team_image.all()]
        return img


class AdminContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


class AdminTopRankStudentSerializer(ModelSerializer):
    class Meta:
        model = TopRankStudent
        fields = '__all__'


class AdminTopRankProfessorSerializer(ModelSerializer):
    professor_images = SerializerMethodField()

    class Meta:
        model = TopRankProfessor
        fields = '__all__'

    def get_professor_images(self, obj):
        return obj.professor_image.url if obj.professor_image else None


class AdminNewsLatterSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
