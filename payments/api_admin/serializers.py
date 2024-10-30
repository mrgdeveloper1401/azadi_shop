from rest_framework.serializers import ModelSerializer, CharField

from ..models import Payment


class AdminPaymentSerializer(ModelSerializer):
    user = CharField()
    course = CharField(source='course.title')

    class Meta:
        model = Payment
        fields = '__all__'
