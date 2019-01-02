# Third Party Stuff
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# milife-back Stuff
from milife_back.base.api.routers import SingletonRouter
from milife_back.users.api import CurrentUserViewSet, UsersViewSet
from milife_back.users.auth.api import AuthViewSet
from milife_back.documents.api import DocumentsViewSet
from milife_back.schedule.api import ScheduleViewSet
from milife_back.fitness.api import WeightViewSet

default_router = DefaultRouter()
singleton_router = SingletonRouter()


# Register all the django rest framework viewsets below.
default_router.register('auth', AuthViewSet, base_name='auth')
singleton_router.register('me', CurrentUserViewSet, base_name='me')


simple_router = routers.SimpleRouter(trailing_slash=False)
simple_router.register('users', UsersViewSet, base_name='users')

nested_user_router = routers.NestedSimpleRouter(simple_router, r'users', lookup='user')

nested_user_router.register('documents', DocumentsViewSet, base_name='user_documents')
nested_user_router.register('schedule', ScheduleViewSet, base_name='user_schedule')
nested_user_router.register('weight', WeightViewSet, base_name='user_weight')

default_router.register('schedule', ScheduleViewSet, base_name='schedule')
default_router.register('weight', WeightViewSet, base_name='weight')

# nested_simple_router = router.NestedSimpleRouter(trailing_slash=False)
# default_router.register('users/{pk}/documents', DocumentsViewSet, base_name="user_documents")6
# simple_router.register('users', UsersViewSet, base_name="users")
# default_router.register('documents', DocumentsViewSet, base_name="documents")



# Combine urls from both default and singleton routers and expose as
# 'urlpatterns' which django can pick up from this module.
urlpatterns = default_router.urls + singleton_router.urls + simple_router.urls + nested_user_router.urls

