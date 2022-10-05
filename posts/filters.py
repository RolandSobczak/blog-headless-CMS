from rest_framework.filters import BaseFilterBackend


class IsAdminFilterBackend(BaseFilterBackend):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self

    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff:
            return queryset
        return queryset.filter(**self.kwargs)
