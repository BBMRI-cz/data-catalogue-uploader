from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client


class Sequencing(MolgenisObject):

    TYPE = "fair-genomes_Sequencing"

    def __init__(self, patient_dict, sample_dict, run_metadata_dict):
        sample = patient_dict["samples"][0]
        self.SequencingIdentifier = sample["pseudo_ID"]
        self.BelongsToSamplePreparation = sample["pseudo_ID"].replace("predictive", "sampleprep")
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
        data = self.serialize
        temp = [data]
        print(type(temp))           # Should be <class 'list'>
        print(len(temp))            # Should be 1
        print(type(temp[0]))        # Should be <class 'dict'>
        print(temp[0].keys())
        print(client.save_schema("sequencing", data=temp))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
