from rest_framework.permissions import BasePermission, SAFE_METHODS


HTTP_METHODS = ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE',)


class IsAuthor(BasePermission):
    def __init__(self, admin_methods: tuple = HTTP_METHODS, attr: str = 'author', other_can_read: bool = True):
        self.admin_methods = admin_methods
        self.attr = attr
        self.other_can_read = other_can_read

    def __call__(self, *args, **kwargs):
        return self

    def has_object_permission(self, request, view, obj):
        return bool(
            (request.method in SAFE_METHODS if self.other_can_read else False) or
            getattr(obj, self.attr) if self.attr else obj == request.user or
            request.user.is_staff and request.method in self.admin_methods
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )