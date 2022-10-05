from rest_framework import serializers


class ObjectExistsValidator:
    def __init__(self, queryset, field: str = "pk"):
        self.queryset = queryset
        self.field = field

    def __call__(self, value):
        valid_values = [getattr(obj, self.field) for obj in self.queryset]
        if value not in valid_values:
            message = f'Object with this {self.field} dosen\'t exists'
            raise serializers.ValidationError(message)