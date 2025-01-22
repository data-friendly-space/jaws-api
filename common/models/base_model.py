"""This module contains the base_model model"""
from abc import abstractmethod, ABCMeta

from django.db import models


class AbstractModelBase(ABCMeta, type(models.Model)):
    """Metaclass combining ABCMeta and ModelBase"""
    pass


class BaseModel(models.Model, metaclass=AbstractModelBase):
    """Base model"""

    class Meta:
        abstract = True

    @classmethod
    def from_tos(cls, TOs):
        """
        Transform a list of TOs into a list of model instances.
        """
        if not TOs:
            return None
        return [cls.from_to(TO) for TO in TOs]

    @abstractmethod
    def from_to(cls, instance):
        """
        Abstract method to transform a TO into a model instance.
        """
        pass
