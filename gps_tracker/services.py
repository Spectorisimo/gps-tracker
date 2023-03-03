from typing import Protocol
from . import models
from django.db.models import QuerySet
from . import repository


class GPSDataServicesInterface(Protocol):

    @staticmethod
    def get_all_data() -> QuerySet[models.GPSData]:
        ...

    @staticmethod
    def get_single_data(pk: int) -> models.GPSData:
        ...


class GPSDataServicesV1():
    gpsdata_repository: repository.GPSDataRepositoryInterface = repository.GPSDataRepositoryV1()

    def get_all_data(self) -> QuerySet[models.GPSData]:
        return self.gpsdata_repository.get_all_data()

    def get_single_data(self,pk: int) -> models.GPSData:
        return self.gpsdata_repository.get_single_data(pk)