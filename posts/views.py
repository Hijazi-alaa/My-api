from django.db.models import Count
from rest_framework import generics, permissions, filters
from arthub_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostsSerializer


class PostList(generics.ListCreateAPIView):
    """
    View list of posts or create a post for logged in users.
    """
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count("comment", distinct=True),
        likes_count=Count("likes", distinct=True)
    ).order_by("-created_at")

    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = [
        "comments_count",
        "likes_count",
        "likes__created_at",
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View a post, and delete or edit if logged in user is owner
    """
    serializer_class = PostsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count("comment", distinct=True),
        likes_count=Count("likes", distinct=True)
    ).order_by("-created_at")
