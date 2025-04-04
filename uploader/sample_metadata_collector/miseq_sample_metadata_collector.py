import json
import re
import os
from .sample_metadata_collector import SampleMetadataCollector, SampleInfoMMCI

class CollectMiseqSampleMetadata(SampleMetadataCollector):

    def __init__(self, run_path, sample_path, catalog_info_path):
        self.sample_info = SampleInfoMMCI()
        self.run_path = run_path
        self.sample_path = sample_path
        self.clinical_data_path = catalog_info_path

    def collect(self) -> SampleInfoMMCI:
        sample_id = os.path.basename(self.sample_path)
        metadata = self._find_sample_metadata(sample_id)

        return metadata

    def _find_sample_metadata(self, sample_id):
        self._find_data_in_statinfo(os.path.join(self.sample_path, "Analysis", f"{sample_id}_StatInfo.txt"))
        self._find_data_in_ccrs(os.path.join(self.sample_path, "Analysis",
                                             "Reports", f"{sample_id}_Coverage_Curve_Report1_Statistics.txt"))
        self._find_data_in_clinical_info(self.clinical_data_path, sample_id)
        return self.sample_info

    def _find_data_in_statinfo(self, txt_stat_info):
        with open(txt_stat_info, 'r', encoding='utf-8', errors="ignore") as f:
            for line in f:
                avr_read_len_match = re.search(r'Average Read Length: ([\d]+)', line)
                if avr_read_len_match:
                    self.sample_info.obsReadLength = avr_read_len_match.group(1)

    def _find_data_in_ccrs(self, txt_ccrs):
        with open(txt_ccrs, 'r', encoding='utf-8', errors="ignore") as f:
            for line in f:
                avr_coverage_match = re.search(r'Average Coverage\s+([\d.,]+)', line)
                if avr_coverage_match:
                    self.sample_info.avReadDepth = float(avr_coverage_match.group(1).replace(",", "."))

    def _find_data_in_clinical_info(self, json_clinical_data, sample_id):
        if os.path.exists(os.path.join(json_clinical_data, f"{sample_id}.json")):
            with open(os.path.join(json_clinical_data, f"{sample_id}.json"), encoding='utf-8') as json_file:
                data = json.load(json_file)
                    
            self.sample_info.idSample = data.get('samples')[0].get('pseudo_ID')
            self.sample_info.collFromPerson = data.get('ID')
            self.sample_info.belToDiag = self.sample_info.collFromPerson[:5] + "clinical" + self.sample_info.collFromPerson[12:]
            material = data.get('samples')[0].get('material_type')
            self.sample_info.pathoState = "NoInformation (NI, nullflavor)"
            if material == "4" or material == "54":
                self.sample_info.pathoState = "Normal"
            if material == "1" or material == "2" or material == "3" or material == "5" or material == "53" or material == "55" or material == "56":
                self.sample_info.pathoState = "Tumor"
            if material == "1" or material == "2" or material == "3" or material == "4" or material == "5":
                self.sample_info.bioSpeciType = "Frozen Tissue"
                self.sample_info.storCond = "Cryotube 1–2mL Programmable freezing to <-135°C"
            if material == "53" or material == "54" or material == "55" or material == "56":
                self.sample_info.bioSpeciType = "Cryopreserved Tissue"
            if material == "7":
                self.sample_info.bioSpeciType = "Cell Pellet"
                self.sample_info.storCond = "Cryotube 1–2mL Programmable freezing to <-135°C"
            if material == "C" or material == "K" or material == "L" or material == "PD" or material == "SD" or material == "T":
                self.sample_info.bioSpeciType = "Serum or Plasma"
                self.sample_info.storCond = "Cryotube 1–2mL Programmable freezing to <-135°C"
            if material == "gD":
                self.sample_info.bioSpeciType = "Blood DNA"
                self.sample_info.storCond = "PP tube 0.5–2mL (-35) to (-18)°C"
            if material == "PK":
                self.sample_info.bioSpeciType = "Peripheral Blood"
                self.sample_info.storCond = "PP tube 0.5–2mL (-35) to (-18)°C"
            if material == "PR":
                self.sample_info.bioSpeciType = "Tumor Cell Line"
                self.sample_info.storCond = "Cryotube 1–2mL Programmable freezing to <-135°C"