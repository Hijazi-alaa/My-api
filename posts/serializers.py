from rest_framework import serializers
from likes.models import Like
from .models import Post


class PostsSerializer(serializers.ModelSerializer):
    """
    The Post model serializer
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        """
        Method to validate acceptable image sizes
        """
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

    def get_like_id(self, obj):
        """
        Get method to register each like with its own id
        """
        user = self.context["request"].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        """
        Meta class for the postsserializer class
        """
        model = Post
        fields = [
            "id", "owner", "is_owner", "profile_id",
            "profile_image", "created_at", "updated_at",
            "title", "description", "image", "image_filter",
            "like_id", "comments_count", "likes_count",
        ]
