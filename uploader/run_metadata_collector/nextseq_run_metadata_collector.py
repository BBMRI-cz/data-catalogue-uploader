import xml.etree.ElementTree as ET
from datetime import date
from .run_metadata_collector import RunMetadataCollector, RunInfoMMCI
import os

class CollectNextSeqRunMetadata(RunMetadataCollector):

    def __init__(self, run_path):
        self.run_path = run_path
        self.run_metadata = RunInfoMMCI()
        self.run_metadata.percentageQ30 = None

    def collect(self):
        run_parameters = os.path.join(self.run_path, "RunParameters.xml")
        if not os.path.exists(run_parameters):
            run_parameters = os.path.join(self.run_path, "runParameters.xml")
        run_completion_status = os.path.join(self.run_path, "RunCompletionStatus.xml")
        run_info = os.path.join(self.run_path, "RunInfo.xml")

        self._find_data_in_run_param(ET.parse(run_parameters))
        self._find_data_run_completion_status(ET.parse(run_completion_status))
        self._find_data_in_run_info(ET.parse(run_info))

        return self.run_metadata

    def _find_data_in_run_param(self, data_tree):          #this function extracts run parameters from file "RunParameters"
        for element in data_tree.iter("RunParameters"):
            self.run_metadata.idMMCI = "nxt_" + element.find("RunNumber").text
            run_date = element.find("RunStartDate").text
            year = 2000 + int(run_date[:2])  # prekonvertovanie roku do celého čísla
            month = int(run_date[2:4])
            day = int(run_date[4:])
            d = date(year, month, day)
            isoformat = d.isoformat()
            self.run_metadata.seqDate = isoformat
            self.run_metadata.seqPlatform = "Illumina platform"
            self.run_metadata.seqMethod = "Illumina Sequencing"
            self.run_metadata.seqModel = "NextSeq 500"
        for element in data_tree.iter("Setup"):
            self.run_metadata.numLanes = element.find("NumLanes").text

    def _find_data_run_completion_status(self, data_tree):   #this function extracts run parameters from file RunCompletionStatus
        for element in data_tree.iter("RunCompletionStatus"):
            self.run_metadata.clusterDensity = element.find('ClusterDensity').text
            self.run_metadata.clusterPF = element.find('ClustersPassingFilter').text
            self.run_metadata.estimatedYield = element.find('EstimatedYield').text
            self.run_metadata.errorDescription = element.find('ErrorDescription').text

    def _find_data_in_run_info(self, data_tree):
        for element in data_tree.iter("Run"):
            self.run_metadata.flowcellID = element.find("Flowcell").text
