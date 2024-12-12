from abc import ABC, abstractmethod


class RunInfoMMCI:

    def __init__(self):
        self.idMMCI: int = 0            #XML_RunParameters
        self.seqDate: str = ''          #XML_RunParameters
        self.seqPlatform: str = "Illumina platform"
        self.seqModel: str = "MiSeq"
        self.seqMethod: str = "Illumina Sequencing"
        self.percentageQ30: str = ''    #AnalysisLog.txt
        self.percentageTR20: str = 'NA'
        self.other: str = '' # commented below

        # self.clusterPF: int = 0         #GemerateFASTQRunStatistics
        # self.numLanes: int = 0          #XML_RunParameters
        # self.flowcellID: str = ''       #XML_RunInfo


class RunMetadataCollector(ABC):

    @abstractmethod
    def collect(self) -> RunInfoMMCI:
        ...
