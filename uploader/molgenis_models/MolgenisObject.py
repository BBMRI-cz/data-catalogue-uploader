from abc import ABC, abstractmethod


class MolgenisObject(ABC):

    @abstractmethod
    def add_to_catalog_if_not_exist(self, session):
        ...

    @property
    def serialize(self):
        d = {}
        for key, value in self.__dict__.items():
            if value.__class__ == tuple:
                d[key] = value[0]
            else:
                d[key] = value
        return d
