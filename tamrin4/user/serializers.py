from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from . import models


class PhoneNumberSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.MyUser
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'user',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=models.MyUser.objects.all(),
                fields=['phone_number', 'user']
            )
        ]
