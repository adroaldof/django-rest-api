from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("id",)

    user = UserSerializer(read_only=True)
