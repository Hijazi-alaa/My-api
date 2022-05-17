from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from arthub_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    """
    Profile view as a list
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request}
            )
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    Class for Profile detail views
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        """
        Getting the Profile by primary key
        and raising error 404 when priamry key is invalid.
        """
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        """
        Get profile by primary key
        using serializers.
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, context={'request': request}
            )
        return Response(serializer.data)


    def put(self, request, pk):
        """
        Put method to edit Profile fields
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

