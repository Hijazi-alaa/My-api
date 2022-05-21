from rest_framework import generics, permissions
from arthub_api.permissions import IsOwnerOrReadOnly
from .models import Post
from .serializers import PostsSerializer

class PostList(generics.ListCreateAPIView):
    """
    View list of posts or create a post for logged in users.
    """
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View a post, and delete or edit if logged in user is owner
    """
    serializer_class = PostsSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
