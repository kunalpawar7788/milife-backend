# Third Party Stuff
from rest_framework import viewsets

# milife-back Stuff
from milife_back.base import response

from . import models, serializers


class CurrentUserViewSet(viewsets.GenericViewSet):
    """Powers the /me endpoint."""
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_active=True)

    def get_object(self):
        return self.request.user

    def list(self, request):
        """Get logged in user profile"""
        serializer = self.get_serializer(self.get_object())
        return response.Ok(serializer.data)

    def partial_update(self, request):
        """Update logged in user profile"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Ok(serializer.data)

class UsersViewSet(viewsets.GenericViewSet):
    """powers admin interface."""
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.filter(is_active=True)

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return response.Ok(serializer.data)

    def retrieve(self, request, pk):
        instance = self.queryset.get(id=pk)
        serializer = self.get_serializer(instance)
        return response.Ok(serializer.data)
