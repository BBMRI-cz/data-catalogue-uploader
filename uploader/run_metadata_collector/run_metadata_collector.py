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

        self.clusterPF: str         #GemerateFASTQRunStatistics
        self.numLanes: str          #XML_RunParameters
        self.flowcellID: str        #XML_RunInfo
        self.clusterDensity: str 
        self.clusterPF: str
        self.estimatedYield: str
        self.errorDescription: str


class RunMetadataCollector(ABC):

    @abstractmethod
    def collect(self) -> RunInfoMMCI:
        ...
