from rest_framework.serializers import ModelSerializer
from . import models


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = models.UrlModel
        fields = '__all__'


class RequestSerializer(ModelSerializer):
    class Meta:
        model = models.UrlModel
        fields = ('url')
