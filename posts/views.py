from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostsSerializer
from arthub_api.permissions import IsOwnerOrReadOnly

class PostList(APIView):
    """
    Post view class
    """
    serializer_class = PostsSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        """
        Post list view
        """
        posts = Post.objects.all()
        serializer = PostsSerializer(
            posts, many=True, context={"request": request}
            )
        return Response(serializer.data)

    def post(self, request):
        """
        post method for the Posts view
        """
        serializer = PostsSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

class PostDetail(APIView):
    """
    Post detail view class
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostsSerializer

    def get_object(self, pk):
        """
        Get method to fetch a post from the post list
        with primary key or return an error
        if it post does not exist
        """
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Get method to retrive a post by id
        """
        post = self.get_object(pk)
        serializer = PostsSerializer(
            post, context={"request": request}
        )
        return Response(serializer.data)


    def put(self, request, pk):
        """
        Put method to enable edit a post
        """
        post = self. get_object(pk)
        serializer = PostsSerializer(
            post, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk):
        """
        method to delete a post
        """
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
