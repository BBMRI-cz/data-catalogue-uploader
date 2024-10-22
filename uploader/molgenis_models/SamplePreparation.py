from ..manage_libraries import LibrariesManager
import re
from uploader.molgenis_models.MolgenisObject import MolgenisObject


class SamplePreparation(MolgenisObject):

    TYPE = "fair-genomes_SamplePreparation"

    def __init__(self, run_path, libraries_path, sample_sheet, patient_dict):
        sample = patient_dict["samples"][0]
        self.SampleprepIdentifier = sample["pseudo_ID"].replace("predictive", "sampleprep")
        self.BelongsToMaterial = sample["sample_ID"]
        lib_data = LibrariesManager(libraries_path, sample_sheet, run_path, sample["pseudo_ID"]).get_data_from_libraries()
        
        if lib_data:
            self.InputAmount = re.sub("[^0-9]", "", lib_data["input_amount"].split("-")[0]) if "-" in lib_data["input_amount"] else re.sub("[^0-9]", "", lib_data["input_amount"])
            self.LibraryPreparationKit = lib_data["library_prep_kit"]
            self.PcrFree = lib_data["pca_free"]
            self.TargetEnrichmentKit = lib_data["target_enrichment_kid"]
            self.UmisPresent = lib_data["umi_present"]
            self.IntendedInsertSize = lib_data["intended_insert_size"]
            self.IntendedReadLength = lib_data["intended_read_length"]
            self.genes = lib_data["genes"]

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["SampleprepIdentifier"] for val in session.get(self.TYPE)]
        if self.SampleprepIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
