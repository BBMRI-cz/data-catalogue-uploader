from abc import ABC

from uploader.molgenis_models.MolgenisObject import MolgenisObject


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

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
