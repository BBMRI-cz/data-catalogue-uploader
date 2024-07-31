import xml.etree.ElementTree as ET
import json
from datetime import date
import re
import os

class RunInfoMMCI:

    def __init__(self):
        self.idMMCI: int = 0            #XML_RunParameters
        self.seqDate: str = ''          #XML_RunParameters
        self.seqPlatform: str = "Illumina platform"    
        self.seqModel: str = "MiSeq"
        self.seqMethod: str = "Illumina Sequencing"
        self.percentageQ30: str = ''    #AnalysisLog.txt
        self.percentageTR20: str = 'NA' #this number is not relevant for MMCI
        self.clusterPF: int = 0         #GemerateFASTQRunStatistics
        self.numLanes: int = 0          #XML_RunParameters
        self.flowcellID: str = ''       #XML_RunInfo


class CollectRunMetadata:

    def __init__(self, run_path):
        self.run_info = RunInfoMMCI()
        self.run_path = run_path

    def __call__(self):
        xml_run_parameters = os.path.join(self.run_path, "runParameters.xml")
        xml_generate_fastq_run_statistics = os.path.join(self.run_path, "GenerateFASTQRunStatistics.xml")
        xml_run_info = os.path.join(self.run_path, "RunInfo.xml")
        txt_analysis_log = os.path.join(self.run_path, "AnalysisLog.txt")

        # /home/houfek/Work/MMCI/sequencing_pipeline/data-catalogue-uploader/tests/test_destination_for_testing/2020/MiSEQ/00000/2020_M00000_0000_00000000-00000/CompletedJobInfo.xml

        if not (os.path.exists(xml_run_parameters) and os.path.exists(xml_generate_fastq_run_statistics)
                and os.path.exists(xml_run_info) and os.path.exists(txt_analysis_log)):
            return False

        run_data = self._find_run_metadata(xml_run_parameters, xml_generate_fastq_run_statistics,
                                           xml_run_info, txt_analysis_log)
        run_metadata = os.path.join(self.run_path, "run_metadata.json")

        with open(run_metadata, 'w') as outfile:
            json.dump(run_data, outfile, indent=4)

        return True

    def _find_run_metadata(self, run_parameters, generate_fastq_run_statistics, run_info, analysis_log):  # fifth_source
        run_parameters_tree = ET.parse(run_parameters)
        self.run_info = self._find_data_in_runparam(run_parameters_tree, self.run_info)
        generate_fastq_run_stat_tree = ET.parse(generate_fastq_run_statistics)
        self.run_info = self._find_data_in_generateFASTQrunstatistics(generate_fastq_run_stat_tree, self.run_info)
        run_info_tree = ET.parse(run_info)
        self.run_info= self._find_data_in_runinfo(run_info_tree, self.run_info)
        self.run_info= self._find_data_in_analysislog(analysis_log, self.run_info)
        json_str = self.run_info.__dict__
        return json_str

    def _find_data_in_runparam(self, run_params_tree, run):
        for element in run_params_tree.iter("RunParameters"):
            run.idMMCI = "mis_" + element.find("RunNumber").text
            run_date = element.find("RunStartDate").text
            year = 2000 + int(run_date[:2])  # prekonvertovanie roku do celého čísla
            month = int(run_date[2:4])
            day = int(run_date[4:])
            d = date(year, month, day)
            isoformat = d.isoformat()
            run.seqDate = isoformat
        for element in run_params_tree.iter("Setup"):
            run.numLanes = int(element.find("NumLanes").text)
        return run

    def _find_data_in_generateFASTQrunstatistics(self, generate_fq_stats_tree, run):
        for element in generate_fq_stats_tree.iter("RunStats"):
            run.clusterPF = element.find("NumberOfClustersPF").text
        run.percentageTR20 = "NA"
        return run

    def _find_data_in_runinfo(self, run_info_tree, run):
        for element in run_info_tree.iter("Run"):
            run.flowcellID = element.find("Flowcell").text
        return run

    def _find_data_in_analysislog(self, analysis_log, run):
        with open(analysis_log, 'r') as f:
            for line in f:
                match = re.search(r'Percent >= Q30: ([\d]{1,2}.[\d]{1,2}\%)', line)
                if match:
                    run.percentageQ30 = match.group(1)
        return run
