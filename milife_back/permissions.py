from rest_framework.permissions import IsAuthenticated, BasePermission

class AllowOptionsAuthentication(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return request.user and request.user.is_authenticated


class NestedUserPermission(BasePermission):

    def has_permission(self, request, view):
        user_pk = request.parser_context['kwargs'].get('user_pk')

        if user_pk and str(request.user.id) != str(user_pk) and not request.user.is_staff:
            return False

        if view.action == 'list':
            return request.user.is_authenticated
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False

        if view.action == 'retrieve':
            return obj.user == request.user or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj.user == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return request.user.is_staff
        else:
            return False


class UsersPermission(BasePermission):
    """
    found at: https://stackoverflow.com/a/34162842/338691
    """
    def has_permission(self, request, view):
        if view.action == 'list':
            print(request.user.is_authenticated , request.user.is_staff)
            return request.user.is_authenticated and request.user.is_staff
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated():
            return False
        if view.action == 'retrieve':
            return obj == request.user or request.user.is_staff
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_staff
        elif view.action == 'destroy':
            return request.user.is_staff
        else:
            return False
