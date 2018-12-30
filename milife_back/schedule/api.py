from rest_framework import viewsets, parsers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response
from . import models, serializers
from milife_back.users.models import User

import uuid

class ScheduleViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.ScheduleSerializer
    queryset = models.Schedule.objects.filter(deleted=False)

    def list(self, request, user_pk=None):
        instances = self.queryset.filter(trainee=request.user)
        serializer = self.serializer_class(instances, many=True)
        return response.Ok(serializer.data)

    def retrieve(self, request, pk, user_pk=None):
        instance = self.queryset.get(id=pk)
        serializer = self.serializer_class(instance)
        return response.Ok(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Created(serializer.data)
        return response.BadRequest(serializer.error)

    def update(self, request, pk):
        pass

    def delete(self, request, pk):
        instance = self.queryset.get(id=pk)
        instance.deleted=True
        instance.save()
        return response.Gone()
