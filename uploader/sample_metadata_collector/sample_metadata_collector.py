from abc import ABC, abstractmethod


class SampleInfoMMCI:

    def __init__(self):
        self.idSample: str = ''
        self.collFromPerson: str = ''
        self.belToDiag: str = ''
        self.bioSpeciType: str = ''
        self.pathoState: str = ''
        self.storCond: str = ''
        self.wsiAvailability: bool = False
        self.radioDataAvailability: bool = False
        self.avReadDepth: str = '' # Data z analýz takže NA pro NextSeq
        self.obsReadLength: str = '' # Data z analýz takže NA pro NextSeq

class SampleMetadataCollector(ABC):

    @abstractmethod
    def collect(self):
        ...
