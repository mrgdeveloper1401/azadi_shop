from rest_framework.serializers import ModelSerializer

from ..models import Image


class AdminImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
