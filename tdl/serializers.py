from django.contrib.auth import get_user_model
from rest_framework import serializers

from tdl.validators import ItemValidator

from .models import ItemList

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = ['id', 'name', 'completed', 'user', 'user_links']

    user = serializers.StringRelatedField(read_only=True)
    user_links = serializers.HyperlinkedRelatedField(
        source='user',
        view_name='tdl:item_api_user_detail',
        read_only=True
    )

    def validate(self, attrs):
        super_validate = super().validate(attrs)

        ItemValidator(data=attrs, validation_error=serializers.ValidationError)

        return super_validate
