from uploader.logging_config.logging_config import LoggingConfig
from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client


class Sequencing(MolgenisObject):

    TYPE = "fair-genomes_Sequencing"

    def __init__(self, patient_dict, sample_dict, run_metadata_dict):
        sample = patient_dict["samples"][0]
        self.SequencingIdentifier = sample["pseudo_ID"]
        self.BelongsToSample = sample["pseudo_ID"].replace("predictive", "sampleprep")
        self.SequencingDate = run_metadata_dict.seqDate
        self.SequencingPlatform = run_metadata_dict.seqPlatform
        self.SequencingInstrumentModel = run_metadata_dict.seqModel
        self.SequencingMethod = run_metadata_dict.seqMethod
        self.MedianReadDepth = sample_dict.avReadDepth
        self.ObservedReadLength = sample_dict.obsReadLength
        self.PercentageQ30 = run_metadata_dict.percentageQ30.replace("%", "") if run_metadata_dict.percentageQ30 else None
        self.OtherQualityMetrics = run_metadata_dict.other

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["SequencingIdentifier"] for val in session.get(self.TYPE)]
        if self.SequencingIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def upsert_to_catalog(self, client: Client):
        logger = LoggingConfig.get_logger()
        data = self.serialize
        logger.info(client.save_schema("sequencing", data=[data]))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
