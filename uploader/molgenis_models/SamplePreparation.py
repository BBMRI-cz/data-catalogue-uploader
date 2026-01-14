import re
from uploader.logging_config.logging_config import LoggingConfig
from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client


class SamplePreparation(MolgenisObject):

    TYPE = "fair-genomes_SamplePreparation"

    def __init__(self, run_path, patient_dict, lib_data):
        sample = patient_dict["samples"][0]
        self.SampleprepIdentifier = sample["pseudo_ID"].replace("predictive", "sampleprep")
        self.BelongsToMaterial = sample["sample_ID"]
        
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

    def upsert_to_catalog(self, client: Client):
        logger = LoggingConfig.get_logger()
        data = self.serialize
        logger.info(client.save_schema("samplepreparation", data=[data]))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
