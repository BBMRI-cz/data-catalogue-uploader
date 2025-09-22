from abc import ABC, abstractmethod
from molgenis_emx2_pyclient import Client
import pandas as pd


class MolgenisObject(ABC):

    @abstractmethod
    def add_to_catalog_if_not_exist(self, session):
        ...

    @abstractmethod
    def upsert_to_catalog(self, client: Client):
        ...

    @property
    def serialize(self):
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, tuple):
                d[key.lower()] = value[0]
            else:
                d[key.lower()] = value
        return d
