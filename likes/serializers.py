from django.db import IntegrityError
from rest_framework import serializers
from likes.models import Like


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model
    """
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        """
        meta class for the LikeSerializer
        """
        model = Like
        fields = ["id", "created_at", "owner", "post"]

    def create(self, validated_data):
        """
        create method to return a complete object instance
        based on the validated data
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "possible duplicate"
            })
