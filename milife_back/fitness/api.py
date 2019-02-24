from rest_framework import viewsets, parsers, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response, mixins
from milife_back.permissions import NestedUserPermission
from . import models, serializers
from django.contrib.auth import get_user_model

import uuid


class NestedQuerysetMixin(object):
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(user=str(user_pk))
        return self.queryset


class WeightViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.WeightSerializer
    queryset = models.Weight.objects.all()
    permission_classes = (NestedUserPermission,)


class ProgrammeViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ProgrammeSerializer
    permission_classes = ()


class MessageViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classes = ()


class MealPlanViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MealPlanSerializer
    permission_classes = ()


# class SessionViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.SessionSerializer


class CheckinViewSet(NestedQuerysetMixin, viewsets.ModelViewSet):
    parsers = (parsers.FileUploadParser, )
    serializer_class = serializers.CheckinSerializer
    queryset = models.Checkin.objects.all()
    lookup_field = "date_of_checkin"

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        client = get_user_model().objects.get(id=user_pk)
        context = {
            'user': client
        }
        super_context.update(context)
        return super_context


    # @permission_classes((IsAdminUser,))
    # def create(self, request, user_pk):
    #     client = get_user_model().objects.get(id=user_pk)
    #     data = dict(**request.data)
    #     data['user'] = uuid.UUID(str(client.id))

    #     serializer = self.serializer_class(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     else:
    #         print(serializer.errors)
    #     return response.Created()

