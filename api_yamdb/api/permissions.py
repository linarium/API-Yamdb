from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (not request.user.is_anonymous
                    and request.user.is_admin))


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (not request.user.is_anonymous
                and request.user.is_admin)


class IsAuthorAdminModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or not request.user.is_anonymous)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (not request.user.is_anonymous
                    and (request.user == obj.author
                         or request.user.is_admin
                         or request.user.is_moderator)))
