from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import bleach


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)


    def pre_save(self, model_instance, add):
        current_value = getattr(model_instance, self.attname)
        try:
            qs = self.model.objects.all()
            if self.for_fields:
                query = {field: getattr(model_instance, field) for field in self.for_fields}
                qs = qs.filter(**query)
            last_item = qs.latest(self.attname)
            last_item_value = getattr(last_item, self.attname)
            if current_value is None:
                current_value = last_item_value + 1
            elif current_value - last_item_value > 1:
                current_value = last_item_value + 1
            elif qs := qs.filter(order=current_value):
                obj = qs.first()
                obj.order += 1
                obj.save()
        except ObjectDoesNotExist:
            value = 0
        setattr(model_instance, self.attname, current_value)
        return super(OrderField, self).pre_save(model_instance, add)


class HTMLField(models.TextField):
    description = 'Clean HTML field'

    def pre_save(self, model_instance, add):
        current_value = getattr(model_instance, self.attname)
        if type(current_value) == str:
            cleaned_value = bleach.clean(current_value)
        else:
            cleaned_value = None
        setattr(model_instance, self.attname, cleaned_value)
        return super(HTMLField, self).pre_save(model_instance, add)