from rest_framework import serializers
from .models import Post

class PostsSerializer(serializers.ModelSerializer):
    """
    The Post model serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')


    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                "Image size larger than 2MB"
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                "Image width larger than 4096px"
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                "Image height larger than 4096px"
            )
        return value

    def get_is_owner(self, obj):
        """
        Check if the user
        is owner of the post and return
        results
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Post
        fields = [
            "id", "owner", "is_owner", "profile_id",
            "profile_image", "created_at", "updated_at",
            "title", "description", "image", "image_filter"
        ]
