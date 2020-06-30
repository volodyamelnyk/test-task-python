from rest_framework import serializers
from .models import Request, BlockedDomain


class RequestSerializer(serializers.ModelSerializer):

    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = Request
        fields = '__all__'


class BlockedDomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlockedDomain
        fields = '__all__'
