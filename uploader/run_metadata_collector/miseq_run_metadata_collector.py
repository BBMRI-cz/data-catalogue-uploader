import xml.etree.ElementTree as ET
from datetime import date
import re
import os
from .run_metadata_collector import RunMetadataCollector, RunInfoMMCI


class CollectMiseqRunMetadata(RunMetadataCollector):

    def __init__(self, run_path):
        self.run_info = RunInfoMMCI()
        self.run_path = run_path

    def collect(self) -> RunInfoMMCI:
        xml_run_parameters = os.path.join(self.run_path, "RunParameters.xml")
        if not os.path.exists(xml_run_parameters):
            xml_run_parameters = os.path.join(self.run_path, "runParameters.xml")
        xml_generate_fastq_run_statistics = os.path.join(self.run_path, "GenerateFASTQRunStatistics.xml")
        xml_run_info = os.path.join(self.run_path, "RunInfo.xml")
        txt_analysis_log = os.path.join(self.run_path, "AnalysisLog.txt")

        self._find_run_metadata(xml_run_parameters, xml_generate_fastq_run_statistics, xml_run_info, txt_analysis_log)

        return self.run_info

    def _find_run_metadata(self, run_parameters, generate_fastq_run_statistics, run_info, analysis_log):  # fifth_source
        run_parameters_tree = ET.parse(run_parameters)
        self._find_data_in_runparam(run_parameters_tree)

        generate_fastq_run_stat_tree = ET.parse(generate_fastq_run_statistics)
        self._find_data_in_generate_fastq_runstatistics(generate_fastq_run_stat_tree)

        run_info_tree = ET.parse(run_info)
        self._find_data_in_run_info(run_info_tree)

        self._find_data_in_analysis_log(analysis_log)

    def _find_data_in_runparam(self, run_params_tree):
        for element in run_params_tree.iter("RunParameters"):
            self.run_info.idMMCI = "mis_" + element.find("RunNumber").text
            run_date = element.find("RunStartDate").text
            year = 2000 + int(run_date[:2])  # prekonvertovanie roku do celého čísla
            month = int(run_date[2:4])
            day = int(run_date[4:])
            d = date(year, month, day)
            isoformat = d.isoformat()
            self.run_info.seqDate = isoformat
        for element in run_params_tree.iter("Setup"):
            self.run_info.numLanes = element.find("NumLanes").text

    def _find_data_in_generate_fastq_runstatistics(self, generate_fq_stats_tree):
        for element in generate_fq_stats_tree.iter("RunStats"):
            self.run_info.clusterPF = element.find('NumberOfClustersPF').text
        self.run_info.percentageTR20 = "NA"

    def _find_data_in_run_info(self, run_info_tree):
        for element in run_info_tree.iter("Run"):
            self.run_info.flowcellID = element.find("Flowcell").text

    def _find_data_in_analysis_log(self, analysis_log):
        with open(analysis_log, 'r') as f:
            for line in f:
                match = re.search(r'Percent >= Q30: (\d{1,2}.\d{1,2}%)', line)
                if match:
                    self.run_info.percentageQ30 = match.group(1)
