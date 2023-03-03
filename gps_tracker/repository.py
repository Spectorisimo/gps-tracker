from typing import Protocol
from . import models
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


class GPSDataRepositoryInterface(Protocol):

    @staticmethod
    def get_all_data() -> QuerySet[models.GPSData]:
        ...

    @staticmethod
    def get_single_data(pk: int) -> models.GPSData:
        ...


class GPSDataRepositoryV1():

    def get_all_data(self) -> QuerySet[models.GPSData]:
        return models.GPSData.objects.all()

    def get_single_data(self, pk: int) -> models.GPSData:
        return get_object_or_404(models.GPSData, pk=pk)
