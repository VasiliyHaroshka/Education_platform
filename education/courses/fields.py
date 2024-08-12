from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """
    Modified django PositiveIntegerField
    """

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields  # специальное поле для упорядочения данных
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """Calculation of special field's value before save object in data base"""
        if getattr(model_instance, self.attname) is None:  # проверка наличия значения у поля порядка
            try:
                qs = self.model.objects.all()  # набор querysets для извлечения всех объектов модели поля
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
