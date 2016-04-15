from django.db import models
from django.utils import timezone


class DeleteMixin(object):
    """
    Overrides delete and sets `is_deleted=True` instead of deleting object.
    Intended to be used with models that have an `is_deleted` field.
    """
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class BaseModelManager(models.Manager):
    """
    Model manager intended to be used with models with an `is_deleted` field.
    Overrides the initial QuerySet to filter for objects where `is_deleted`
    is false.
    """
    def get_queryset(self):
        return (super(BaseModelManager, self).get_queryset()
                .filter(is_deleted=False))


class BaseModel(DeleteMixin, models.Model):
    """
    Abstract base class models which defines created_at and is_deleted fields.

    Attributes:
        created_at (datetime.datetime):
            Datetime at which the model is created.
        is_deleted (boolean):
            If value is True, mdoel is deleted. Default is False.
    """
    objects = BaseModelManager()

    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True