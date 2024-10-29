from rest_framework.serializers import ModelSerializer

from professors.models import Professor


class AdminProfessorSerializer(ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'
