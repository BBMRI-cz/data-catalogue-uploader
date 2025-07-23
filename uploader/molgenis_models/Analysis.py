from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client


class Analysis(MolgenisObject):

    TYPE = "fair-genomes_Analysis"

    def __init__(self, patient_dict):
        sample = patient_dict["samples"][0]
        self.AnalysisIdentifier = sample["pseudo_ID"].replace("predictive", "analysis")
        self.BelongsToSequencing = sample["pseudo_ID"]
        self.PhysicalDataLocation = "Masaryk Memorial Cancer Istitute"
        self.AbstractDataLocation = "Sensitive Cloud Institute of Computer Science"
        self.DataFormatsStored = ["BAM", "VCF"]
        self.ReferenceGenomeUsed = "GRCh37"
        self.BioinformaticProtocolUsed = "NextGENe"

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["AnalysisIdentifier"] for val in session.get(self.TYPE)]
        if self.AnalysisIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def upsert_to_catalog(self, client: Client):
        data = self.serialize
        temp = [data]
        print(type(temp))           # Should be <class 'list'>
        print(len(temp))            # Should be 1
        print(type(temp[0]))        # Should be <class 'dict'>
        print(temp[0].keys())
        print(client.save_schema("analysis", data=temp))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
