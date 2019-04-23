from rest_framework import viewsets, parsers, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from milife_back.base import response, mixins
from milife_back.permissions import NestedUserPermission
from . import models, serializers
from django.contrib.auth import get_user_model

import uuid


class NestedUserQuerysetMixin(object):
    def get_queryset(self):
        user_pk = self.kwargs.get('user_pk')
        if user_pk:
            return self.queryset.filter(user=str(user_pk))
        return self.queryset

class NestedProgrammeQuerysetMixin(object):
    def get_queryset(self):
        pk = self.kwargs.get('programme_pk')
        if pk:
            return self.queryset.filter(programme=str(pk))
        return self.queryset


class WeightViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.WeightSerializer
    queryset = models.Weight.objects.all()
    permission_classes = (NestedUserPermission,)

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'user_ref': user,
        }
        super_context.update(context)
        return super_context


class TargetWeightViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.TargetWeightSerializer
    queryset = models.TargetWeight.objects.all()
    permission_classes = (NestedUserPermission,)

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'user_ref': user
        }
        super_context.update(context)
        return super_context


class ProgrammeViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ProgrammeSerializer
    queryset = models.Programme.objects.all()
    permission_classes = ()


class HolidayViewSet(NestedProgrammeQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.HolidaySerializer
    queryset = models.Holiday.objects.all()
    permission_classes = ()


class SessionLedgerViewSet(NestedProgrammeQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.SessionLedgerSerializer
    queryset = models.SessionLedger.objects.all()
    permission_classes = ()


class MessageViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
    permission_classes = (NestedUserPermission,)

    def get_serializer_context(self, ):
        super_context = super().get_serializer_context()
        user_pk = self.kwargs['user_pk']
        user = get_user_model().objects.get(id=user_pk)
        context = {
            'recipient': user,
            "sender": self.request.user
        }
        super_context.update(context)
        return super_context


class MealPlanViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MealPlanSerializer
    permission_classes = ()


# class SessionViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.SessionSerializer


class CheckinViewSet(NestedUserQuerysetMixin, viewsets.ModelViewSet):
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

