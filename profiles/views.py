from django.db.models import Count
from rest_framework import generics, filters
from arthub_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    class view to view list of all profile
    """
    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer

    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = [
        "posts_count",
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View a profile or update it if the user is the owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count("owner__post", distinct=True),
    ).order_by("-created_at")
    serializer_class = ProfileSerializer
