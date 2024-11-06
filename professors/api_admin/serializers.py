from rest_framework.serializers import ModelSerializer, SerializerMethodField

from professors.models import Professor


class AdminProfessorSerializer(ModelSerializer):
    professor_url = SerializerMethodField()

    class Meta:
        model = Professor
        fields = '__all__'

    def get_professor_url(self, obj):
        return obj.professor_image.url if obj.professor_image else None
